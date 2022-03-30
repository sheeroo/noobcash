from block import Block
from time import time

class Blockchain:

    def __init__(self):
        self.chain = []
        self.curr_transactions = []
        self.nodes = set()
        self.genesis_block()
    
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
            curr_transactions=self.curr_transactions,
            previous_hash=previous_hash,
            timestamp=time.time()
        )

        #reset current transactions
        self.curr_transactions = []
        
        #add block to blockchain
        self.chain.append(block)

        return block
    
    def validate_chain(self):
        '''Validates the chain calling validate block for each block

        Returns:
            Boolean: False if any one block is not validated
        '''
        for block in self.chain:
            if block.index != 0 and not block.validate_block(prev):
                return False
            prev = block

    @property
    def last_block(self):
        '''Get last block of chain
        Returns:
            Block: last block of chain
        '''
        return self.chain[-1]