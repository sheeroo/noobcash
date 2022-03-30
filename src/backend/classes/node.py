import hashlib
import os
from threading import Thread
import requests
from block import Block
from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet

class Node:
	def __init__(self, ip, port, wallet):
		self.blockchain = Blockchain()
		self.wallet = wallet or Wallet()
		self.ring = []
		self.utxo = []
		self.port = port
		self.ip = ip
		self.cancel_mining = False
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
			response = requests.post(f'{bootstrap_ip}:{bootstrap_port}/subscribe', 
				data={
					'ip': self.ip,
					'port': self.port,
					'public_key': self.wallet.public_key
				}
			)
			response_data = response.json()
			self.id = response_data['id']
		except requests.HTTPError as errorh:
			print(f'Oops, {errorh}')
			raise Exception(f'Cannot subscribe to bootstrap node due to {errorh}')
		except requests.ConnectionError as error:
			print(f'Oops, {error}')
			raise Exception(f'Cannot subscribe to bootstrap node due to {error}')
		
	''' Wallet is being created in init '''
	# def create_wallet(self):
	# 	#create a wallet for this node, with a public key and a private key
	# 	self.wallet = Wallet()

	# def balance(self,recipient, utxos):

	# 	amount = 0
	# 	for utxo in utxos:
	# 		amount += utxo
		
	# 	return amount

	# def create_transaction(sender, receiver, signature):
	# 	#remember to broadcast it


	# def broadcast_transaction(self):

	# def validate_transaction(self):
	# 	#use of signature and NBCs balance

	# def broadcast_block(self):

	def create_transaction(self, receiver, amount):

		if self.wallet.public_key == receiver:
			raise Exception('You cannot send money to yourself dumdum!')
		if amount <= 0:
			raise Exception('You must send something dumdum!')
		
		transaction_inp = []
		total = 0
		
		for utxo in self.utxo:
			if (total < amount):
				if (utxo['receiver'] == self.wallet.public_key.decode()):
					total += utxo['amount']
					transaction_inp.append(utxo)
			else:
				break
		
		if total >= amount:
			transaction = Transaction(self.wallet.public_key, self.wallet.private_key, receiver, amount, transaction_inp)
			
		if amount > total:
			raise Exception('Insufficient funds dumdum!')
		
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
			if self.valid_proof(new_block.current_hash):
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

	#concencus functions

	# def valid_chain(self, chain):
	# 	#check for the longer chain across all nodes

	# def resolve_conflicts(self):
	# 	#resolve correct chain

	# def register_node_to_ring(self):
	# 	#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
	# 	#boοtstrap node informs all other nodes and gives the request node an id and 100 NBCs
	
	@classmethod
	def fromDictionary(nodeDict):
		wallet = Wallet(public_key=nodeDict['public_key'], private_key='')
		return Node(
			ip=nodeDict['ip'],
			port=nodeDict['port'],
			wallet=wallet
		)

	def broadcast(self, url_action, data, responses):
		'''Generic broadcast function using POST http method
		Args:
			url_action (String): Url to hit on other nodes,
			data (Dict): Dictionary to hit body
		Returns:
			array of responses
		'''
		threads=[]
		responses=[]
		def call_func(node, url_action, data, responses):
			response = requests.post(f'{node.ip}:{node.port}/{url_action}', data=data)
			responses.append(response)
		for node in self.ring:
			thread=Thread(target=call_func, args=(node, url_action, data, responses))
			threads.append(thread)
			thread.start()

		for thread in threads:
			thread.join()
		return responses