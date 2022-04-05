from crypt import methods
import os
import threading
import time
from flask import Flask, Blueprint, jsonify, request, render_template
from flask_cors import CORS
from utils.debug import log
from classes.block import Block
from classes.transaction import Transaction
from exceptions.block import AlreadyReceivedBlockException, InvalidBlockException
from exceptions.transaction import InsufficientFundsException, InvalidTransactionException

# from classes.block import Block
from classes.node import Node
# from classes.blockchain import Blockchain
# from classes.wallet import Wallet
# from classes.transaction import Transaction
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

app = Flask(__name__)
CORS(app)

# Process memory 
node: Node = None

bootstrap = Blueprint('bootstrap', __name__)
@bootstrap.route('/subscribe', methods=['POST'])
def subscribe():
    if not node.is_bootstrap:
        response = { 'error': True, 'message': "I ain't bootstrap m8" }
        return jsonify(response), 400
    else:
        data = request.json
    # Get node data from request body heh
        new_node = Node.from_dict(data)
        id = node.register_node_to_ring(new_node)

        response = { 'id': id, 'state': node.state }

        return jsonify(response), 200

@bootstrap.route('/healthcheck', methods=['POST'])
def healthcheck():
    '''If a node calls this he has definetely subscribed so make the transaction
    '''
    if not node.is_bootstrap:
        response = { 'error': True, 'message': "I ain't bootstrap m8" }
        return jsonify(response), 400
    else:
        data = request.json
    # Get node data from request body heh
        new_node = Node.from_dict(data)

        receiver_pub = new_node.wallet.public_key.decode()

        node.create_transaction(receiver_pub, 100)

        response = { 'error': False }
        return jsonify(response), 200

transaction = Blueprint('transactions', __name__, url_prefix='/transaction')
@transaction.route('/receive', methods=['POST'])
def receive_transaction():
    transaction_dict = request.json
    transaction = Transaction.from_dict(transaction_dict)

    node.tx_queue_lock.acquire()
    log.info(f'Acquired first lock ({threading.get_ident()})...')
    if len(node.tx_queue) == 0 or transaction.timestamp > node.tx_queue[-1].timestamp:
        log.info('Appending to transaction queue...')
        node.tx_queue.append(transaction)
    else:
        # Insert at proper position according to timestamp
        i = 0
        log.info('Finding correct position for this transaction...')
        while transaction.timestamp > node.tx_queue[i].timestamp:
            i+=1
        node.tx_queue.insert(i, transaction)
    
    node.tx_queue_lock.release()
    log.info(f'Sleeping ({threading.get_ident()})...')
    # Sleep to exploit flask multithreading and locking for other requests capture by threads to insert their transactions
    time.sleep(0.5)
    node.tx_queue_lock.acquire()
    log.info(f'Acquired second lock ({threading.get_ident()})...')
    new_transaction = node.tx_queue.pop(0)

    node.utxo_lock.acquire()
    log.info(f'Acquired utxo lock ({threading.get_ident()})...')
    try:
        node.validate_transaction(new_transaction)
        node.add_transaction_to_block(new_transaction)
        response = { 'transaction_outputs': [u.to_dict() for u in new_transaction.transaction_outputs] }
        return jsonify(response), 200
    except InvalidTransactionException as e:
        response = { 'error': True, 'message': e.message }
        return jsonify(response), 400

@transaction.route('/create', methods=['POST'])
def create_transaction():
    data=request.json()
    receiver = data['receiver']
    amount = data['amount']

    try:
        node.create_transaction(receiver, amount)
    except InsufficientFundsException as ife:
        response = { 'error': True, 'message': ife.message }
        log.error(response)
        return jsonify(response), 400
    except Exception as e:
        response = { 'error': True, 'message': e.message }
        log.error(response)
        return jsonify(response), 400

block = Blueprint('/block', __name__, url_prefix='/block')
@block.route('/receive', methods=['POST'])
def receive_block():
    # Stop mining
    node.cancel_mining = True

    block_dict = request.json
    block = Block.from_dict(block_dict)
    last_block: Block = None
    # Check if block's transactions are already received in another block
    block_transactions = [t.transaction_id for t in block.transactions]
    try:
        with node.tx_log_lock:
        # If same transactions are already received
            for t in block_transactions:
                if t in node.tx_log[::-1]:
                    raise AlreadyReceivedBlockException(block=block)
            
            node.tx_log.extend(block_transactions)
            # Wait while concensus is running
            while node.resolving_conflict:
                pass

            with node.blockchain_lock:
                last_block = node.blockchain.last_block
                if block.index in [b.index for b in node.blockchain.chain]:
                    raise AlreadyReceivedBlockException(block=block)
            
        # Here only if block is not already broadcasted from another minder
        block.validate_block(last_block)
        node.blockchain.chain.append(block)
        response = { 'error': False, 'message': 'Block accepted' }
        return jsonify(response), 200
    except AlreadyReceivedBlockException as e:
        response = { 'error': True, 'message': e.message }
        return jsonify(response), 200
    except InvalidBlockException as ie:
        response = { 'error': True, 'message': ie.message }
        return jsonify(response), 200

debug = Blueprint('debug', __name__, url_prefix='/debug')
@debug.route('/node', methods=['GET'])
def print_node():
    return jsonify(node.to_dict()), 200

@debug.route('/blockchain', methods=['GET'])
def print_blockchain():
    return jsonify(node.blockchain.to_dict()), 200

app.register_blueprint(bootstrap)
app.register_blueprint(transaction)
app.register_blueprint(block)
app.register_blueprint(debug)

if __name__ == '__main__':
    from argparse import ArgumentParser

    # Get bootstrap node data from environment
    bootstrap_ip = os.getenv('BOOTSTRAP_IP')
    bootstrap_port = int(os.getenv('BOOTSTRAP_PORT'))

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    parser.add_argument('-ip', '--ipaddress', default='127.0.0.1', type=str, help='my ip')
    args = parser.parse_args()
    port = args.port
    ip = args.ipaddress

    def init(ip, port, bootstrap_ip, bootstrap_port):
        global node
        if not node:
        # Create a new node
            node = Node(ip=ip, port=port)
            log.info(f'Starting node -> {ip}:{port}')

            if ip == bootstrap_ip and port == bootstrap_port:
                # You are the bootstrap node
                node.id = 0
                # Create genesis block
                node.genesis_block()
                # Add bootstrap to ring
                # node.ring.append(node)
                log.info('You are the bootstrap node')
                log.info(node)
                log.info(node.blockchain.last_block.__str__(), header='Genesis block')
            else:
                # Try to subscribe to bootstrap node
                node.subscribe(bootstrap_ip=bootstrap_ip, bootstrap_port=bootstrap_port)
    
    thread=threading.Thread(target=init, args=(ip, port, bootstrap_ip, bootstrap_port))
    thread.start()
    app.run(host='127.0.0.1', port=port, threaded=True)
