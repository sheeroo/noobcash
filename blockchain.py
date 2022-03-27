import block
import threading

class Blockchain:

    def __init__(self):
        self.chain = []
        self.lock = threading.Lock()
    
    def add_block(self, block):
        self.chain.append(block)