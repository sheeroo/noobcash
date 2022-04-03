import json
import os
from .utxo import Utxo
from .block import Block
from .transaction import Transaction
from exceptions.block import InvalidBlockException
from exceptions.blockchain import InvalidBlockchainException
from time import time
from utils.debug import log

class Blockchain:

    def __init__(self, chain=None, transactions_log=None):
        self.chain = chain or []
        self.transactions_log = transactions_log or [] # log transactions while mining ?
        self.checkpoint = 0
    
    def genesis_block(self, bootstrap_address):
        '''Constructs the genesis block
        
        Returns:
            Block: the genesis block (nonce = 0 and previous hash = 1)
        '''
        block = self.construct_block(nonce=0, previous_hash=1)
        nodes = int(os.getenv('NODES'))
        amount = 100*nodes

        transaction_outputs = Utxo(
            previous_trans_id=0,
            amount=amount,
            recipient=bootstrap_address
        )

        genesis_transaction = Transaction(
            sender_address=0,
            sender_private_key=0,
            receiver_address=bootstrap_address,
            amount=amount,
            transaction_inputs=[],
            transaction_outputs=[transaction_outputs]
        )

        block.add_transaction(genesis_transaction, self)
        return 

    def construct_block(self, nonce, previous_hash):
        '''Constructs a new block after PoW and appends it to the blockchain

        Args:
            nonce (int): a number produced during the creation of a new block
            previous_hash (string): the hash of the previous block

        Returns:
            Block: the created block
        '''
        block = Block(
            index=len(self.chain),
            nonce=nonce,
            curr_transactions=self.transactions_log,
            previous_hash=previous_hash,
            timestamp=time.time()
        )

        #reset current transactions
        self.transactions_log = []
        
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
        after_chekpoint = list(map(Block.from_dict, dictionary['chain']))
        result_chain = before_checkpoint.extend(after_chekpoint)
        log.info(result_chain, header='Result chain: ')

        transaction_log = map(Transaction.from_dict, dictionary['transaction_log'])

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
    
    def to_dict(self, checkpoint):
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

    @classmethod
    def from_dict(dictionary: dict):
        result_chain = list(map(Block.from_dict, dictionary['chain']))
        log.info(dictionary, header='Blockchain received dict: ')
        return Blockchain(
			chain=result_chain
		)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)


