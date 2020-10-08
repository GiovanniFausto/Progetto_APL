
from hashlib import sha256
import json
import time

class Block:
    def __init__(self, index, transazioni, timestamp, hashPrecedente, nonce=0):
        self.index = index
        self.transazioni = transazioni
        self.timestamp = timestamp
        self.hashPrecedente = hashPrecedente
        self.nonce = nonce

    def calcoloHash(self):    
        block = json.dumps(self.__dict__, sort_keys=True) #__dict__ contiene tutti gli attributi di block
        hashBlock = sha256(block.encode()).hexdigest()
        return hashBlock
    
    #@staticmethod
    """def createGenesisBlock(self):
        genesisBlock = Block(0, [], time.time(), "0")
        genesisBlock.hash = self.compute_hash()
        return genesisBlock"""