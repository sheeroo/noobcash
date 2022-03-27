import block
import blockchain
import rest
import transaction
import wallet

import threading

class node:
	def __init__(self, port, N, ip):

		self.chain = blockchain.Blockchain()
		self.wallet = wallet.Wallet()
		self.ring = []
		self.utxo = []
		self.port = port
		self.ip = ip
		#self.current_id_count
		#self.NBCs
		#self.wallet

	def create_genesis_block(self):
		if self.id == 0:
			#do stuff
			return 0
		else:
			raise Exception('Node is not bootstrap node')

	def create_new_block(self):
		self.chain.lock.acquire()
		#add new block
		self.chain.lock.release()
		
		return new_block

	def create_wallet(self):
		#create a wallet for this node, with a public key and a private key

	def balance(self,recipient, utxos):

		amount = 0
		for utxo in utxos:
			amount += utxo
		
		return amount

	def register_node_to_ring(self):
		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs


	def create_transaction(sender, receiver, signature):
		#remember to broadcast it


	def broadcast_transaction(self):

	def validdate_transaction(self):
		#use of signature and NBCs balance


	def add_transaction_to_block(self):
		#if enough transactions  mine



	def mine_block(self):



	def broadcast_block(self):


		

	def valid_proof(.., difficulty=MINING_DIFFICULTY):




	#concencus functions

	def valid_chain(self, chain):
		#check for the longer chain accroose all nodes


	def resolve_conflicts(self):
		#resolve correct chain



