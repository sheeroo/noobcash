from socket import socket
from flask_socketio import SocketIO, emit
from email import message
import os
import threading
import time
from urllib import response
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
socketio = SocketIO(app, engineio_logger=True, logger=True, cors_allowed_origins="*", path='/socket.io')
CORS(app)


# Process memory 
node: Node = None
isLoggedIn = False

bootstrap = Blueprint('bootstrap', __name__, url_prefix='/bootstrap')
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
    log.info(f'Receiving transaction {transaction.transaction_id}...')

    while node.resolving_conflict:
        pass

    node.tx_queue_lock.acquire()
    log.info(f'Acquired first lock ({threading.get_ident()})...')
    if len(node.tx_queue) == 0 or transaction.timestamp > node.tx_queue[-1].timestamp:
        # log.info('Appending to transaction queue...')
        node.tx_queue.append(transaction)
    else:
        # Insert at proper position according to timestamp
        i = 0
        # log.info('Finding correct position for this transaction...')
        while transaction.timestamp > node.tx_queue[i].timestamp:
            i+=1
        node.tx_queue.insert(i, transaction)
    
    node.tx_queue_lock.release()
    # log.info(f'Sleeping ({threading.get_ident()})...')
    # Sleep to exploit flask multithreading and locking for other requests capture by threads to insert their transactions
    time.sleep(0.5)
    # Block adding new transactions while mining but do not hold the lock for sorting newly received transactions
    while node.mining:
        pass

    with node.tx_queue_lock:
        # log.info(f'Acquired second lock ({threading.get_ident()})...')
        new_transaction = node.tx_queue.pop(0)

        with node.utxo_lock:
            # log.info(f'Acquired utxo lock ({threading.get_ident()})...')
            try:
                node.validate_transaction(new_transaction)
                node.add_transaction_to_block(new_transaction)
                response = { 'error': False, 'message': f'Transaction {new_transaction.transaction_id} received' }
                return jsonify(response), 200
            except InvalidTransactionException as e:
                response = { 'error': True, 'message': e.message }
                return jsonify(response), 400

@transaction.route('/create', methods=['POST'])
def create_transaction():
    data=request.json
    receiver_id = data['receiver']
    amount = data['amount']
    receiver = None
    try:
        for r in node.ring:
            if r.id == receiver_id:
                receiver = r.wallet.public_key.decode()
        if receiver == None:
            raise InvalidTransactionException(message='No node with such id found')
        created_transaction = node.create_transaction(receiver, amount)

        response = { 'error': False, 'message': f'Transaction created with id {created_transaction.transaction_id}'}
        return jsonify(response), 200
    except InsufficientFundsException as ife:
        response = { 'error': True, 'message': ife.message }
        log.error(response)
        return jsonify(response), 400
    except InvalidTransactionException as e:
        response = { 'error': True, 'message': e.message }
        return jsonify(response), 400
    except Exception as e:
        response = { 'error': True, 'message': 'An unknown error occured' }
        log.error(e)
        return jsonify(response), 400

block = Blueprint('/block', __name__, url_prefix='/block')
@block.route('/receive', methods=['POST'])
def receive_block():
    # Stop mining
    node.mining = False

    block_dict = request.json
    block = Block.from_dict(block_dict)
    last_block: Block = None

    log.info(f'Receiving block {block.index}...')
    # Check if block's transactions are already received in another block
    block_transactions = [t.transaction_id for t in block.transactions]
    try:
        with node.tx_log_lock:
        # If same transactions are already received
            for t in block_transactions:
                if t in node.tx_log[::-1]:
                    raise AlreadyReceivedBlockException(block, message='Block transactions already in log')
            
            node.tx_log.extend(block_transactions)
            # Wait while concensus is running
            while node.resolving_conflict:
                pass

            with node.blockchain_lock:
                last_block = node.blockchain.last_block
                if block.index in [b.index for b in node.blockchain.chain]:
                    raise AlreadyReceivedBlockException(block, message='Block index already in chain')
            
        # Here only if block is not already broadcasted from another minder
        block.validate_block(last_block)
        node.blockchain.chain.append(block)
        response = { 'error': False, 'message': 'Block accepted' }
        return jsonify(response), 200
    except AlreadyReceivedBlockException as e:
        response = { 'error': True, 'message': e.message }
        return jsonify(response), 200
    except InvalidBlockException as ie:
        # If block is invalid then resolve conflict
        if ie.message == "This block has invalid previous hash":
            node.resolve_conflict()
        response = { 'error': True, 'message': ie.message }
        return jsonify(response), 200

ring = Blueprint('/ring', __name__, url_prefix='/ring')
@ring.route('/receive', methods=['POST'])
def receive_ring():
    req_json = request.json
    ring = [Node.from_dict(r) for r in req_json['ring']]
    node.ring = ring
    response = {'error': False, 'message': 'Received ring'}
    return jsonify(response), 200

@app.route('/state/get', methods=['POST'])
def get_state():
    return jsonify(node.state), 200

@app.route('/balance', methods=['GET'])
def get_balance():
    balance = node.wallet_balance()
    response = { 'balance': balance }
    return jsonify(response), 200

@app.route('/login', methods=['GET'])
def login():
    if isLoggedIn:
        response = { 'error': True, 'message': 'Someone is already logged in' }
        return jsonify(response), 401
    else:
        response = { 'error': False, 'message': f'Welcome back to node {node.id}'}
        return jsonify(response), 200
    
@app.route('/logout', methods=['POST'])
def logout():
    if isLoggedIn:
        isLoggedIn = False
        response = { 'error': False, 'message': f'Successfully disconnected from node {node.id}'}
        return jsonify(response), 200
    else:
        response = { 'error': True, 'message': 'No one is connected to this node' }
        return jsonify(response), 400

debug = Blueprint('debug', __name__, url_prefix='/debug')
@debug.route('/node', methods=['GET'])
def print_node():
    return jsonify(node.to_dict()), 200

@debug.route('/blockchain', methods=['GET'])
def print_blockchain():
    return jsonify(node.blockchain.to_dict()), 200

@debug.route('/finalstate', methods=['GET'])
def print_finalstate():
    result = []
    for r in node.ring:
        result.append({
            'node': r.id,
            'balance': node.wallet_balance(r.public_key)
        })
    return jsonify(result), 200

@debug.route('/sendhello', methods=['GET'])
def send_hello():
    socketio.emit('hello', {'sheeesh': 'Hellooo'}, broadcast=True)
    return jsonify({'ok': True}), 200

app.register_blueprint(bootstrap)
app.register_blueprint(transaction)
app.register_blueprint(ring)
app.register_blueprint(block)
app.register_blueprint(debug)

@socketio.on('hello')
def print_hello():
    log.success('HELLOOO')

# @socketio.on('connect')
# def test_connect(auth):
#     emit('my response', {'data': 'Connected'})
    
@socketio.on_error()
def error_handler(e):
    print('An error has occurred: ' + str(e))

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
                node_copy = Node(ip=node.ip, port=node.port, wallet=node.wallet) # Do not take ring of current node object
                node_copy.id = node.id
                node.ring.append(node_copy)
                log.info('You are the bootstrap node')
                # log.info(node)
                # log.info(node.blockchain.last_block.__str__(), header='Genesis block')
            else:
                # Try to subscribe to bootstrap node
                node.subscribe(bootstrap_ip=bootstrap_ip, bootstrap_port=bootstrap_port)
    
    thread=threading.Thread(target=init, args=(ip, port, bootstrap_ip, bootstrap_port))
    thread.start()
    # app.run(host='127.0.0.1', port=port, threaded=True)
    socketio.run(app, host='127.0.0.1', port=port)
