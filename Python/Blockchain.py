from hashlib import sha256
import json
import time
from Block import Block

class Blockchain:

    # difficoltà scelta per l'algoritmo di Proof of work
    difficultyPoW = 2

    #costrutt bc
    def __init__(self):
        self.transazioniUnconfirmed = [] # lista transazioni da inserire in bc
        self.chain = []  # lista della catena
        self.createGenesisBlock() #creazione blocco genesi, che ha indice 0
    
    def createGenesisBlock(self):       
        genesisBlock = Block(0, [], time.time(), "0")
        self.chain.append(genesisBlock) #aggiunge il blocco genesi alla lista della chain
    
    #per estrarre un nuovo blocco, dopo il blocco genesi
    def createBlock(self, block, proof):

        #verifico se l'hash del nuovo blocco è valido, cioè se soddisfa il vincolo di iniziare con 00
        if proof[:Blockchain.difficultyPoW] != '0' * Blockchain.difficultyPoW: 
            return False

        block.hash = proof #associa l'hash corretto, verificato dal pow al blocco
        self.chain.append(block) # aggiunge il nuovo blocco alla catena
        

    
    # incrementa il nonce di 1 finchè non ottiene un hash
    # che rispetta il criterio di difficoltà impostato (due zeri iniziali).
    def PoW(self, block):
        block.nonce = 0    #inizializza a 0 il nonce   
        hashBlock = block.hash # prende l'hash del nuovo blocco

        # finchè non viene trovato un hash che inizia per 00, viene incrementato il nonce e calcolato un nuovo hash
        while hashBlock[:Blockchain.difficultyPoW] != '0' * Blockchain.difficultyPoW:
            block.nonce += 1
            hashBlock = block.calcoloHash()
        
        return hashBlock

    # serve per creare il nuovo blocco, che contiene la transazione in sospeso che 
    # deve essere inserita al suo interno, dopo aver verificato il pow. 
    # restituisce l'indice del nuovo blocco.
    def mine(self):
        if len(self.transazioniUnconfirmed) == 0: # controlliamo se la lista è vuota
            print("Non ci sono transazioni da confermare")
            return False
        
        ultimoBlocco = self.chain[-1] #prendo l'ultimo blocco presente nella catena
        indice = len(self.chain) # indice del nuovo blocco
        transazioni=self.transazioniUnconfirmed.pop(0) #elimina la transazione dalla lista delle transazioni non conferm
        timestamp=time.time() #tempo corrente
        hashPrecedente = ultimoBlocco.hash #prende l'hash dell'ultimo blocco
        
        nuovoBlocco = Block(indice, transazioni, timestamp, hashPrecedente)
        proof = self.PoW(nuovoBlocco) # verifichiamo il proof of work
        
        self.createBlock(nuovoBlocco, proof) #crea il blocco
        

    #stampa la bc
    def stampa(self):
        for block in self.chain:
            block.stampa()

    #restituisce tutta la catena
    def getChain(self):
        chain = []
        for block in self.chain:
            chain.append(block.__dict__)
        return chain