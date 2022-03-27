import random
import blockchain
import datetime
import hashlib

class Block:
    def __init__(self, index, prev_hash, list_of_transactions):
        ##set self.prev_hash self.timestamp self.hash self.nonce self.list_of_transactions
        self.index = index
        self.timestamp = datetime.datetime.timestamp(datetime.now())
        self.transactions = list_of_transactions
        self.previous_hash = prev_hash
        self.current_hash = self.curr_hash()

        #if bootstrap node (index = 0) then nonce = 0
        if index == 0:
            self.nonce = 0
        else:
            self.nonce = random.randit(1, 2**32 - 1)

    def curr_hash(self):
        
        block_of_string = "{}{}{}{}{}".format(self.prev_hash, self.nonce, self.list_of_transactions, self.timestamp)
        hash = hashlib.sha256(block_of_string.encode()).hexdigest()
        
        return hash

    # def add_transaction(Transaction transaction, Blockchain blockchain):
        #add a transaction to the block