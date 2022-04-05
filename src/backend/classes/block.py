# import blockchain
import json
from operator import index
import time
import hashlib
import os
from utils.debug import log
from exceptions.block import InvalidBlockException
from .transaction import Transaction

class Block:
    def __init__(self, index, previous_hash, nonce, current_hash=None, curr_transactions=None, timestamp=None):
        self.index = index
        self.timestamp = timestamp or time.time()
        self.transactions = curr_transactions or []
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.current_hash = current_hash or self.my_hash()

    def my_hash(self):
        '''Calculates the hash string produced by block's properties

        Returns:
            The unique hash
        '''
        # Using ids instead of object in transactions to avoid different block hash between nodes
        transaction_table = sum(int(t.transaction_id, 16) for t in self.transactions)
        block_of_string = "{}{}{}{}".format(self.previous_hash, self.nonce, transaction_table, self.timestamp)
        return hashlib.sha256(block_of_string.encode()).hexdigest()

    def add_transaction(self, transaction: Transaction):
        #add a transaction to the block
        self.transactions.append(transaction)
        #update current hash
        self.current_hash = self.my_hash()

    def validate_block(self, previous_block):
        '''Validates a block by checking it's hash and previous hash
        Args:
            The previous block

        Returns:
            Boolean: False if block is not valid
        '''
        # Check if current_hash is correct
        if self.current_hash != self.my_hash():
            raise InvalidBlockException(self, block=self, message="This block has invalid hash")
        # Check if previous_hash is equal to previous block's hash
        elif self.previous_hash != previous_block.current_hash:
            raise InvalidBlockException(self, block=self, message="This block has invalid previous hash")
        return True

    def to_dict(self):
        transactions = [t.to_dict() for t in self.transactions]

        return dict(
            index=self.index,
            nonce=self.nonce,
            current_hash=self.current_hash,
            previous_hash=self.previous_hash,
            timestamp=self.timestamp,
            transactions=transactions
        )

    @staticmethod
    def from_dict(blockDict: dict):
        return Block(
            index=blockDict['index'],
            nonce=blockDict['nonce'],
            previous_hash=blockDict['previous_hash'],
            transactions=blockDict['transactions'],
            current_hash=blockDict['current_hash']
        )

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __repr__(self):
        transactions_str = ''
        for i, t in enumerate(self.transactions):
            transactions_str += '\t' + i + '. ' + t.__repr__
        return  'Index: ' + self.index + '\n' \
            +   'Timestamp: ' + self.timestamp + '\n' \
            +   'Hash: ' + self.hash + '\n' \
            +   'Transactions: \n' + transactions_str
