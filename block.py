
# import blockchain
from operator import index
from time import time
import hashlib
import os

class Block:
    def __init__(self, index, previousHash, current_hash, nonce, listOfTransactions, timestamp):
        ##set self.previousHash self.timestamp self.hash self.nonce self.listOfTransactions
        self.index = index
        self.timestamp = timestamp or time.time()
        self.transactions = listOfTransactions
        self.nonce = nonce
        self.previous_hash = previousHash
        self.current_hash = current_hash or self.myHash()

    def myHash(self):
        '''Calculates the hash string produced by block's properties

        Returns:
            The unique hash
        '''
        block_of_string = "{}{}{}{}{}".format(self.previousHash, self.nonce, self.listOfTransactions, self.timestamp)
        return hashlib.sha256(block_of_string.encode()).hexdigest()

    def add_transaction(self, transaction, blockchain):
        #add a transaction to the block
        self.transactions.add(transaction)

    def validate_block(self, previous_block):
        '''Validates a block by checking it's hash and previous hash
        Args:
            The previous block

        Returns:
            Boolean: False if block is not valid
        '''
        # Check if current_hash is correct
        if self.current_hash != self.myHash():
            return False
        # Check if previous_hash is equal to previous block's hash
        elif self.previous_hash != previous_block.current_hash:
            return False
        return True

    def toDictionary(self):
        return dict(
            index=self.index,
            nonce=self.nonce,
            current_hash=self.current_hash,
            previous_hash=self.previous_hash,
            timestamp=self.timestamp,
            transactions=self.transactions
        )

    @classmethod
    def fromDictionary(blockDict):
        return Block(
            index=blockDict['index'],
            nonce=blockDict['nonce'],
            previousHash=blockDict['previous_hash'],
            listOfTransactions=blockDict['transactions'],
            current_hash=blockDict['current_hash']
        )