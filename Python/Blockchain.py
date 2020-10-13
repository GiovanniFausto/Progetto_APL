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
        self.chain.append(genesisBlock)
    
    #per estrarre un nuovo blocco, dopo il blocco genesi
    def createBlock(self, block, proof):
        ultimoBlocco = self.chain[-1]
        hashPrecedente = ultimoBlocco.hash
        #verifico se l'hash inizia con 00

        if not self.validPoW(proof):
            return False

        block.hash = proof #associa l'hash corretto, verificato dal pow al blocco
        self.chain.append(block)
        return True

    
    # incrementa il nonce di 1 finchè non ottiene un hash
    # che rispetta il criterio di difficoltà impostato (due zeri iniziali).
    def PoW(self, block):
        block.nonce = 0       
        hashBlock = block.hash

        while not hashBlock[:Blockchain.difficultyPoW] == '0' * Blockchain.difficultyPoW:
            block.nonce += 1
            hashBlock = block.calcoloHash()
        
        return hashBlock
    
    # verifico se hashBlock ha un hash valido per il blocco
    # il vincolo che deve soddisfare l'hash è che deve iniziare con due 0
    # ritorna True quando lo trova
    def validPoW(self, hashBlock):    
        hashOk = (hashBlock[:Blockchain.difficultyPoW] == '0' * Blockchain.difficultyPoW)
        return (hashOk)

#------Mining-----#
    # serve per creare il nuovo blocco, che contiene la transazione in sospeso che 
    # deve essere inserita al suo interno, dopo aver verificato il pow. 
    # restituisce l'indice del nuovo blocco.
    def mine(self):
        if not self.transazioniUnconfirmed:
            return False
        
        ultimoBlocco = self.chain[-1]
        indice = len(self.chain)
        transazioni=self.transazioniUnconfirmed.pop(0)
        timestamp=time.time()
        hashPrecedente = ultimoBlocco.hash
        
        nuovoBlocco = Block(indice, transazioni, timestamp, hashPrecedente)
        proof = self.PoW(nuovoBlocco)
        
        self.createBlock(nuovoBlocco, proof)
        
        return True

    #stampa la bc
    def stampa(self):
        for block in self.chain:
            block.stampa()