import json
import os

from .utxo import Utxo
from .block import Block
from .transaction import Transaction
from exceptions.block import InvalidBlockException
from exceptions.blockchain import InvalidBlockchainException
import time
from utils.debug import log

class Blockchain:

    def __init__(self, chain=None, transactions_log=None):
        self.chain = chain or []
        self.transactions_log = transactions_log or [] # log transactions while mining ?
        self.checkpoint = 0
    
    def construct_block(self, nonce, previous_hash):
        '''Constructs a new block after PoW and appends it to the blockchain

        Args:
            nonce (int): a number produced during the creation of a new block
            previous_hash (string): the hash of the previous block

        Returns:
            Block: the created block
        '''
        # No current transactions because while mining transactions are receiving 
        block = Block(
            index=len(self.chain),
            nonce=nonce,
            previous_hash=previous_hash,
            timestamp=time.time()
        )
        
        #add block to blockchain
        self.chain.append(block)

        return block
    
    def validate_chain(self):
        '''Validates the chain calling validate block for each block

        Returns:
            Boolean: True if every block is validated
        Raises: 
            InvalidBlockchainException: if any block is not valid to cause * Consensus *
        '''
        try:
            for block in self.chain:
                if block.index != 0:
                    block.validate_block(prev) # Will throw exception if not valid
                prev = block # Get previous block
            return True
        except InvalidBlockException as e:
            raise InvalidBlockchainException(blockchain=self, block=e.block)

    @property
    def last_block(self):
        '''Get last block of chain
        Returns:
            Block: last block of chain
        '''
        return self.chain[-1]

    def resolve(self, dictionary: dict):
        '''Runs after you chose the biggest blockchain after your checkpoint

        Args: 
            dictionary(dict): transmitted JSON object
        '''
        log.info(dictionary, header='Blockchain sent dict: ')

        before_checkpoint = self.chain[:self.checkpoint]
        after_chekpoint = [Block.from_dict(b) for b in dictionary['chain']]
        result_chain = before_checkpoint.extend(after_chekpoint)
        log.info(result_chain, header='Result chain: ')

        transaction_log = [Transaction.from_dict(t) for t in dictionary['transaction_log']]

        log.info([transaction.__str__() for transaction in transaction_log])

        self.transactions_log = transaction_log

# class utilities
    def to_dict(self):
        result_chain = [block.to_dict() for block in self.chain]
        result_transactions_log = [transaction.to_dict() for transaction in self.transactions_log]
        return dict(
            chain=result_chain,
            transactions_log=result_transactions_log
        )
    
    def to_dict_with_checkpoint(self, checkpoint):
        '''To dict overloaded with checkpoint argument to take chain from checkpoint index and after

        Args:
            chekckpoint (int): Sent on concensus from the node requesting the chain
        Returns:
            (dict): dictionary data to be sent through network to run concensus
        '''
        result_chain = [block.to_dict() for block in self.chain[checkpoint:]]
        result_transactions_log = [transaction.to_dict() for transaction in self.transactions_log]
        return dict(
            chain=result_chain,
            transactions_log=result_transactions_log
        )

    @staticmethod
    def from_dict(dictionary: dict):
        result_chain = [Block.from_dict(b) for b in dictionary['chain']]
        log.info(dictionary, header='Blockchain received dict: ')
        return Blockchain(
			chain=result_chain
		)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)


