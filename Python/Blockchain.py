from hashlib import sha256
import json
import time
from Block import Block

class Blockchain:

    # difficoltà scelta per l'algoritmo di Proof of work
    difficultyPoW = 2

    #costrutt bc
    def __init__(self):
        self.transazioniUnconfirmed = [] # transazione da inserire in bc
        self.chain = []
        self.createGenesisBlock() #creazione blocco genesi, che ha indice 0
    
    def createGenesisBlock(self):
        
        genesisBlock = Block(0, [], time.time(), "0")
        genesisBlock.hash = genesisBlock.calcoloHash()
        self.chain.append(genesisBlock)
    
    #per estrarre un nuovo blocco, dopo il blocco genesi
    def createBlock(self, block, proof):
        
        hashPrecedente = self.lastBlock.hash
        #verifico se l'hash inizia con 00
        if not self.validPoW(proof):
            return False
        block.hash = proof #associa l'hash corretto, verificato dal pow al blocco
        #self.transazioniUnconfirmed = [] #resetta la lista delle transazioni non confermate
        self.chain.append(block)
        return True

    @property
    def lastBlock(self):
        return self.chain[-1]
    
    # incrementa il nonce di 1 finchè non ottiene un hash
    # che rispetta il criterio di difficoltà impostato (due zeri iniziali).
    #@staticmethod
    def PoW(self, block):
        #print("DENTRO POW")
        block.nonce = 0       
        hashBlock = block.calcoloHash()
        print("HASH ULTIMO BLOCCO: ", hashBlock)
        #while not self.validPoW(self.transazioniUnconfirmed, hashBlock, nonce):
        while not hashBlock[:Blockchain.difficultyPoW] == '0' * Blockchain.difficultyPoW:
            block.nonce += 1
            hashBlock = block.calcoloHash()
        
        print("HASH CON 00 : ", hashBlock)
        print("NONCE POW: ", block.nonce)
        return hashBlock
    
    # verifico se hashBlock ha un hash valido per il blocco
    # il vincolo che deve soddisfare l'hash è che deve iniziare con due 0
    # ritorna True quando lo trova
    #@classmethod
    def validPoW(self, hashBlock):    
        hashOk = (hashBlock[:Blockchain.difficultyPoW] == '0' * Blockchain.difficultyPoW)
        #print("HASH OK: ", hashOk) 
        return (hashOk )

#------Mining-----#
    # le transazioni create non sono ancora confermate, per cui non possono essere
    # inserite nel blocco. attendono in una coda di transazioni non confermate
    # fino a quando non vengono confermate.
    """def aggiungiTransazione(self, transazione):
            self.transazioniUnconfirmed.append(transazione)"""

    # serve per creare il nuovo blocco, che contiene la transazione in sospeso che 
    # deve essere inserita al suo interno, dopo aver verificato il pow. 
    # restituisce l'indice del nuovo blocco.
    def mine(self):
        if not self.transazioniUnconfirmed:
            return False
        print("dentro mine")
        ultimoBlocco = self.lastBlock
        indice = len(self.chain)
        transazioni=self.transazioniUnconfirmed.pop(0)
        timestamp=time.time()
        #nonce = self.PoW()
        hashPrecedente = ultimoBlocco.hash
        #print("hash precedente: ", hashPrecedente)
        
        nuovoBlocco = Block(indice, transazioni, timestamp, hashPrecedente)
        proof = self.PoW(nuovoBlocco)
        #nonce = self.PoW(nuovoBlocco)
        self.createBlock(nuovoBlocco, proof)
        
        return True