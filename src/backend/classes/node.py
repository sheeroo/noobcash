import hashlib
import os
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
		self.port = port
		self.ip = ip
		self.cancel_mining = False
		self.id = None
		#self.id to be set later
		#self.current_id_count
		#self.NBCs
		#self.wallet

	def is_bootstrap(self):
		return self.id == 0

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
		helper.broadcast(self.ring, '/transaction/receive', transaction.to_dict(), responses)

	def broadcast_block(self, block: Block):
		responses = []
		helper.broadcast(self.ring, '/block/receive', block.to_dict(), responses)

	def validate_transaction(self, transaction: Transaction):
		#use of signature and NBCs balance
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
			self.utxos = [utxo for utxo in self.utxo if utxo.id not in utxos_used]

			# Add transaction outputs
			self.utxos.extend(transaction_outputs)

			return True
		except InvalidTransactionException as e:
			raise e

	def create_transaction(self, receiver, amount):

		if self.wallet.public_key == receiver:
			raise Exception('You cannot send money to yourself dumdum!')
		if amount <= 0:
			raise Exception('You must send something dumdum!')
		
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
		
		transaction = Transaction(self.wallet.public_key, self.wallet.private_key, receiver, amount, transaction_inp)
		# Broadcast transaction
		self.broadcast_transaction(transaction)
		return transaction

	def add_transaction_to_block(self, transaction):
		'''Add a transaction to block or trigger mining
		Args:
			transaction (Transaction): Broadcasted transaction
		'''
		capacity = int(os.getenv('MAX_CAPACITY'))
		last_block = self.blockchain.last_block()
		if len(last_block.transactions) < capacity:
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
		self.cancel_mining = False # Re initialize cancel mining to False to allow mining
		nonce = 0
		new_block = None 
		while True: 
			if self.cancel_mining:
				break
			new_block = Block(
				index=previous_block.index + 1,
				previous_hash=previous_block.current_hash,
				nonce=nonce,
				curr_transactions=[transaction]
			)
			if Node.valid_proof(new_block.current_hash):
				self.brodcast_block(new_block)
				break
			nonce += 1

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

	# def valid_chain(self, chain):
	# 	#check for the longer chain across all nodes

	# def resolve_conflicts(self):
	# 	#resolve correct chain

	# def register_node_to_ring(self):
	# 	#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
	# 	#boοtstrap node informs all other nodes and gives the request node an id and 100 NBCs
	def to_dict(self):
		return dict(
			ip=self.ip,
			port=self.port,
			public_key=self.wallet.public_key.decode()
		)
	
	@staticmethod
	def from_dict(nodeDict: dict):
		wallet = Wallet(public_key=nodeDict['public_key'], private_key='')
		return Node(
			ip=nodeDict['ip'],
			port=nodeDict['port'],
			wallet=wallet
		)

	def __str__(self):
		ring = ''
		for i in self.ring:
			ring += i.__str__()
		return f'{Decoration.UNDERLINE}Node:{Decoration.CLEAR} \n\tid -> {self.id} \n\tring -> [{ring}]'
