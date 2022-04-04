import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from exceptions.transaction import InsufficientFundsException
from noobcash.src.backend.classes.transaction import Transaction
from utils.debug import log

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
node = None

# get all transactions in the blockchain

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    transactions = node.transactions

    response = { 'transactions': transactions }
    return jsonify(response), 200

@app.route('/subscribe', methods=['POST'])
def subscribe():
    if not node.is_bootstrap:
        response = { 'error': True, 'message': "I ain't bootstrap m8" }
        return jsonify(response), 400
    else:
        data = request.json
    # Get node data from request body heh
        new_node = Node.from_dict(data)
        id = node.register_node_to_ring(new_node)

        response = { 'id': id }
        '''
            Need to implement the transaction to give initial 100 NBC to this node!!
        '''

        first_transaction = Transaction(
            node.wallet.public_key.decode(),
            node.wallet.private_key.decode(),
            new_node.wallet.public_key,
            100,
            node.utxo
        )

        new_node.create_transaction(first_transaction)
        new_node.add_transaction_to_block(first_transaction)

        return jsonify(response), 200

@app.route('/transaction/create', methods=['POST'])
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

@app.route('/debug/node', methods=['GET'])
def print_node():
    log.info(node)
    return jsonify(node.to_dict()), 200

@app.route('/debug/blockchain', methods=['GET'])
def print_blockchain():
    log.info(node.blockchain)
    return jsonify(node.blockchain.to_dict()), 200

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
    
    if not node:
        # Create a new node
        node = Node(ip=ip, port=port)
        log.info(f'Starting node -> {ip}:{port}')

        if ip == bootstrap_ip and port == bootstrap_port:
            # You are the bootstrap node
            node.id = 0
            # Create genesis block
            log.info('You are the bootstrap node')
            log.info(node)
        else:
            # Try to subscribe to bootstrap node
            node.subscribe(bootstrap_ip=bootstrap_ip, bootstrap_port=bootstrap_port)

    app.run(host='127.0.0.1', port=port, threaded=True)
