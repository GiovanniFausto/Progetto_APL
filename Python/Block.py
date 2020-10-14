
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
                self.codice=transazioni["Codice"]
                self.categorieDomande = transazioni["CategorieDomande"]
                self.punteggioDomande = transazioni["PunteggioDomande"]
            else:
                self.nome = None
                self.cognome = None
                self.categorieDomande = None
                self.punteggioDomande = None
                
    #serve a calcolare hash
    def calcoloHash(self):    
        block = json.dumps(self.__dict__, sort_keys=True) #__dict__ contiene tutti gli attributi di block
        hashBlock = sha256(block.encode()).hexdigest()
        return hashBlock
    #serve per stampare tutte le info del blocco
    def stampa(self):
        print(self.__dict__)
    #serve per prendere nome cognome e codice, serve poi nelle dataframe
    def infoCandidato(self):
        return self.nome+"_"+self.cognome+"_"+self.codice
    
