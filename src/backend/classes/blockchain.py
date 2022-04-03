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
    
    def genesis_block(self):
        '''Constructs the genesis block
        
        Returns:
            Block: the genesis block (nonce = 0 and previous hash = 1)
        '''
        return self.construct_block(nonce=0, previous_hash=1)

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

# class utilities
    def to_dict(self):
        result_chain = [block.to_dict() for block in self.chain]
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


