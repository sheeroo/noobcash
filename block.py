
# import blockchain
from time import time
import hashlib

class Block:
    def __init__(self, index, previousHash, nonce, listOfTransactions, timestamp):
        ##set self.previousHash self.timestamp self.hash self.nonce self.listOfTransactions
        self.index = index
        self.timestamp = timestamp or time.time()
        self.transactions = listOfTransactions
        self.nonce = nonce
        self.previous_hash = previousHash
        self.current_hash = self.myHash()

    def myHash(self):
        block_of_string = "{}{}{}{}{}".format(self.previousHash, self.nonce, self.listOfTransactions, self.timestamp)
        self.hash = hashlib.sha256(block_of_string.encode()).hexdigest()

    # def add_transaction(Transaction transaction, Blockchain blockchain):
        #add a transaction to the block

    def validate_block(self, previous_block):
        # Check if current_hash is correct
        if self.current_hash != self.myHash():
            return False
        # Check if previous_hash is equal to previous block's hash
        elif self.previous_hash != previous_block.current_hash:
            return False
        return True
