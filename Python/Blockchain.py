from hashlib import sha256
import json
import time


class Blockchain:

    # difficoltà scelta per l'algoritmo di Proof of work
    difficultyPoW = 2

    #costrutt bc
    def __init__(self):
        self.transazioniUnconfirmed = []  # transazione da inserire in bc
        self.chain = []
        self.block(0, [], time.time(), 0, '00') #creazione blocco genesi, che ha indice 0

    # per aggiungere un nuovo blocco alla catena, dopo il blocco genesi
    def block(self, indice, transazioni, timestamp, nonce, hashPrecedente):
        newBlock = {'indice': len(self.chain) + 1,
                'timestamp': time.time(),
                'transazioni': self.transazioniUnconfirmed,
                'nonce': nonce,
                'hashPrecedente': hashPrecedente}
        # resetta la lista delle transazioni
        self.transazioniUnconfirmed = []

        self.chain.append(newBlock)
        return newBlock

    # funzione che calcola l'hash
    @staticmethod
    def calcoloHash(block):
            blockString = json.dumps(block, sort_keys=True).encode()          
            computeHash = sha256(blockString)
            return computeHash.hexdigest()
    
    #serve dopo per sapere l'indice dell'ultimo blocco inserito, da usare per la creazione del nuovo blocco
    #@property
    def lastBlock(self):
        return self.chain[-1]
    
    
    # incrementa il nonce di 1 finchè non ottiene un hash
    # che rispetta il criterio di difficoltà impostato (due zeri iniziali).
    #@staticmethod
    def PoW(self, difficultyPoW = difficultyPoW):
        #print("DENTRO POW")
        nonce = 0
        ultimoBlocco = self.lastBlock()
        hashBlock = self.calcoloHash(ultimoBlocco)
        
        while not self.validPoW(self.transazioniUnconfirmed, hashBlock, nonce):
            nonce += 1
        #return hashBlock
        print("NONCE POW: ", nonce)
        return nonce
    
    # verifico se hashBlock ha un hash valido per il blocco
    # il vincolo che deve soddisfare l'hash è che deve iniziare con due 0
    # ritorna True quando lo trova
    def validPoW(self, transazioni, hashBlock, nonce, difficultyPoW = difficultyPoW):    
        """return (hashBlock[:difficultyPoW] == ('0' * difficultyPoW) and
                hashBlock == self.calcoloHash(block))"""
        stringa = (str(transazioni)+str(hashBlock)+str(nonce)).encode() # non lo so a che serve, mi piacerebbe scoprirlo
        #print("stringa: ", stringa)
        stringaHash = sha256(stringa).hexdigest()
        return stringaHash[:difficultyPoW] == '0' * difficultyPoW

#------Mining-----#
    # le transazioni create non sono ancora confermate, per cui non possono essere
    # inserite nel blocco. attendono in una coda di transazioni non confermate
    # fino a quando non vengono confermate.
    def aggiungiTransazione(self, transazione):
            self.transazioniUnconfirmed.append(transazione)

    # serve per creare il nuovo blocco, che contiene la transazione in sospeso che 
    # deve essere inserita al suo interno, dopo aver verificato il pow. 
    # restituisce l'indice del nuovo blocco.
    def mine(self):
        if not self.transazioniUnconfirmed:
            return False
        print("dentro mine")
        ultimoBlocco = self.lastBlock()
        indice = len(self.chain) + 1
        transazioni=self.transazioniUnconfirmed
        timestamp=time.time()
        nonce = self.PoW()
        hashPrecedente = self.calcoloHash(ultimoBlocco)
        #print("hash precedente: ", hashPrecedente)
        
        nuovoBlocco = self.block(indice, transazioni, timestamp, nonce, hashPrecedente)
        print("nuovo Blocco: ", nuovoBlocco)
        
        return indice