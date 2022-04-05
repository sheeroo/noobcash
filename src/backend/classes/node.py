from concurrent.futures import thread
import hashlib
import json
import os
from threading import Thread
import threading
import requests
from exceptions.transaction import InsufficientFundsException, InvalidTransactionException
from utils.debug import log, Decoration
from utils import helper
from .block import Block
from .blockchain import Blockchain
from .transaction import Transaction
from .wallet import Wallet
from .utxo import Utxo

class Node:
	def __init__(self, ip, port, wallet=None):
		self.blockchain = Blockchain()
		self.wallet = wallet or self.create_wallet()
		self.ring = []
		self.utxo: list(Utxo) = []
		self.utxo_lock = threading.Lock()
		self.port = port
		self.ip = ip
		self.cancel_mining = False
		self.id = None
		self.tx_queue = []
		self.tx_queue_lock = threading.Lock()
		self.tx_log = []
		self.tx_log_lock = threading.Lock()
		#self.id to be set later
		#self.current_id_count
		#self.NBCs
		#self.wallet

	@property
	def is_bootstrap(self):
		return self.id == 0

	def genesis_block(self):
		'''Constructs the genesis block
        Args:
            bootstrap_node
        Returns:
            Block: the genesis block (nonce = 0 and previous hash = 1)
        '''
		bootstrap_address = self.wallet.public_key.decode()
		genesis_block = self.blockchain.construct_block(nonce=0, previous_hash=1)
		nodes = int(os.getenv('NODES'))
		amount = 100*nodes

		transaction_outputs = Utxo(
            previous_trans_id=0,
            amount=amount,
            recipient=bootstrap_address
        )
		
		genesis_transaction = Transaction(
            sender_address=b'0',
            sender_private_key='0',
			signature=b'0', # Adding to avoid sign_signature to run
            receiver_address=bootstrap_address,
            amount=amount,
            transaction_inputs=[],
            transaction_outputs=[transaction_outputs]
        )

		genesis_block.add_transaction(genesis_transaction)

        # First utxo of node
		self.utxo = [transaction_outputs]

	def subscribe(self, bootstrap_ip, bootstrap_port):
		'''Calls bootstrap node to request id and give life signs
		Args:
			bootstrap_ip (String): IP of bootstrap node
			bootstrap_port (Int): Port of bootstrap node	
		'''
		try:
			response = requests.post(f'http://{bootstrap_ip}:{bootstrap_port}/subscribe', 
				json=self.to_dict()
			)
			response_data = response.json()
			self.id = response_data['id']
			log.success(f'Registered node {self.id} to ring.')
		except requests.HTTPError as errorh:
			log.error(f'Oops, {errorh}')
			raise Exception(f'Cannot subscribe to bootstrap node due to {errorh}')
		except requests.ConnectionError as error:
			log.error(f'Oops, {error}')
			raise Exception(f'Cannot subscribe to bootstrap node due to {error}')
		
	def register_node_to_ring(self, node):
		if len(self.ring):
			next_id = self.ring[-1].id + 1
		else:
			next_id = 1
		node.id = next_id
		self.ring.append(node)
		log.success(f'Registered node {Decoration.REVERSED}{node.id}{Decoration.CLEAR} to ring.')
		return next_id

	''' Wallet is being created in init '''
	def create_wallet(self):
		#create a wallet for this node, with a public key and a private key
		return Wallet()

	def wallet_balance(self, public_key):
		amount = 0
		for utxo in self.utxo:
			if utxo.recipient == public_key:
				amount += utxo.amount
		
		return amount

	def broadcast_transaction(self, transaction: Transaction):
		responses = []
		helper.broadcast(self.ring, '/transactions/receive', transaction.to_dict(), responses)

	def broadcast_block(self, block: Block):
		responses = []
		helper.broadcast(self.ring, '/block/receive', block.to_dict(), responses)

	def validate_transaction(self, transaction: Transaction):
		#use of signature and NBCs balance
		log.info(f'Validating transaction: {transaction.__str__()}...')
		try:
			transaction.verify_signature()
		except InvalidTransactionException as e:
			raise InvalidTransactionException(transaction=transaction, message="Transaction verification failed!")
		
		try:
			utxos_used = []
			for trans_in in transaction.transaction_inputs:
				before = len(utxos_used) #length of utxos_used before iterating utxos of node
				for utxo in self.utxo:
					if utxo.id == trans_in.id and utxo.recipient == transaction.sender_address:
						# utxo is used for this transaction
						utxos_used.append(utxo.id)
				after = len(utxos_used) #length of utxos_used after iterating utxos of node
				# If you don't find a transaction input in node's utxo's invalidate the transaction 
				# Double spending prevention
				if after == before:
					raise InvalidTransactionException(transaction=transaction, message="Transaction input utxos not found!")
			# Reaching here means funds are found in utxos so now we have to produce transaction's outputs
			transaction_outputs = transaction.calculate_outputs()

			# Remove utxos used
			self.utxo = [utxo for utxo in self.utxo if utxo.id not in utxos_used]

			# Add transaction outputs
			self.utxo.extend(transaction_outputs)

			return True
		except InvalidTransactionException as e:
			raise e

	def create_transaction(self, recipient, amount):

		if amount <= 0:
			raise InvalidTransactionException('You must send something dumdum!')
		if self.wallet.public_key.decode() == recipient:
			raise InvalidTransactionException('You cannot send money to yourself dumdum!')
		if recipient not in [i.wallet.public_key.decode() for i in self.ring]:
			raise InvalidTransactionException('Unknown recipient')
		
		transaction_inp = []
		total = 0
		
		for utxo in self.utxo:
			if (total < amount):
				if (utxo.recipient == self.wallet.public_key.decode()):
					total += utxo.amount
					transaction_inp.append(utxo)
			else:
				break
			
		if amount > total:
			raise InsufficientFundsException('Insufficient funds dumdum!')
		
		transaction = Transaction(
			sender_address=self.wallet.public_key, 
			sender_private_key=self.wallet.private_key, 
			receiver_address=recipient, 
			amount=amount, 
			transaction_inputs=transaction_inp
		)
		# Broadcast transaction
		self.broadcast_transaction(transaction)

		self.add_transaction_to_block(transaction)
		return transaction

	def add_transaction_to_block(self, transaction):
		'''Add a transaction to block or trigger mining
		Args:
			transaction (Transaction): Broadcasted transaction
		'''
		capacity = int(os.getenv('MAX_CAPACITY'))
		last_block = self.blockchain.last_block
		if len(last_block.transactions) < capacity and last_block.index != 0:
			last_block.add_transaction(transaction)
		else:
			self.mine_block(last_block, transaction)


	# MINING
	def mine_block(self, previous_block, transaction):
		'''Mine a block with PoW and then broadcast it
		Args:
			previous_block (Block): The previous block (the last of the chain)
			transaction (Transaction): The new transaction
		'''
		log.info('Mining...')
		self.cancel_mining = False # Re initialize cancel mining to False to allow mining
		nonce = 0
		new_block = None 
		while True: 
			if self.cancel_mining:
				log.info('Received block. Stoping...')
				return
			new_block = Block(
				index=previous_block.index + 1,
				previous_hash=previous_block.current_hash,
				nonce=nonce,
				curr_transactions=[transaction]
			)
			if Node.valid_proof(new_block.current_hash):
				# Add it to chain
				self.blockchain.chain.append(new_block)
				#Broadcast the block
				self.broadcast_block(new_block)
				break
			nonce += 1
		log.info('Mined!')

	@staticmethod
	def valid_proof(block_hash):
		'''Check if it is valid proof (hash's first |DIFFICULTY| characters are zero
		Args: 
			block_hash (String): testing block's hash
		Returns:
			Boolean: True if proof of work is valid
		'''
		difficulty = int(os.getenv('DIFFICULTY'))
		return block_hash[:difficulty] == '0' * difficulty

	#concensus functions

	def resolve_conflict(self):
		'''Resolves conflicts by returning the longest chain

		Args:
			nodes(list(Blockchain)): Returned data from requested resolve
		'''
		checkpoint_dict = { 'checkpoint': self.blockchain.checkpoint }
		result = []
		helper.broadcast(self.ring, '/blockchain/get', checkpoint_dict, result)


		max_length = len(self.blockchain.chain)

		for blockchain in result:
			
			chain_length = len(blockchain.chain)

			if chain_length > max_length:
				max_length = chain_length
				resolved_chain = blockchain.chain
			
		if resolved_chain:
			return resolved_chain
		
		return False

	def to_dict(self):
		ring=[node.to_dict() for node in self.ring]
		return dict(
			ip=self.ip,
			port=self.port,
			public_key=self.wallet.public_key.decode(),
			ring=ring
		)
	
	@staticmethod
	def from_dict(nodeDict: dict):
		wallet = Wallet(public_key=nodeDict['public_key'].encode(), private_key='')
		return Node(
			ip=nodeDict['ip'],
			port=nodeDict['port'],
			wallet=wallet
		)

	def __str__(self):
		return json.dumps(self.to_dict(), indent=4)
