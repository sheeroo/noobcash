from utils.debug import log

class NbcException(Exception):
    def __init__(self, message="An error occured"):
        self.message = message
        # log.error(self.__class__, ' -> ', message)
        super().__init__(self.message)
    
    def __str__(self):
        return f'Nb Error -> {self.message}'
