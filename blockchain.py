from block import Block
from time import time
##########################
####### needs work #######
##########################
class Blockchain:

    def __init__(self):
        self.chain = []
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
            previousHash=previous_hash,
            timestamp=time.time()
        )
        self.chain.append(block)
        return block
    
    def validate_chain(self):
        '''Validates the chain calling validate block for each block

        Returns:
            Boolean: False if any one block is not validated
        '''
        for i in self.chain:
            if i.index != 0 and not i.validate_block(prev):
                return False
            prev = i