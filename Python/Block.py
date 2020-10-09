
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
            self.hash = self.calcoloHash()
            if len(transazioni)>0:
                self.nome = transazioni["Nome"]
                self.cognome = transazioni["Cognome"]
                self.categoriaDomande = transazioni["CategoriaDomande"]
                self.punteggio = transazioni["Punteggio"]
            else:
                self.nome = None
                self.cognome = None
                self.categoriaDomande = None
                self.punteggio = None
                
        
    def calcoloHash(self):    
        block = json.dumps(self.__dict__, sort_keys=True) #__dict__ contiene tutti gli attributi di block
        hashBlock = sha256(block.encode()).hexdigest()
        return hashBlock
    
