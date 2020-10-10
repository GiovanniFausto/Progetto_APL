import json
import time
from flask import Flask, request
from Blockchain import Blockchain
import csv
import pandas as pd
import pickle
#import torch
import os

# creiamo delle interfacce per il nodo server.
# usiamo Flask come framework per creare un'applicazione REST
app = Flask(__name__)
# copia della bc per il nodo server
blockchain = Blockchain()

#creiamo gli endpoint

#http://localhost:8000/nuovaTransazione 
# serve per creare una nuova transazione in un blocco
@app.route('/nuovaTransazione', methods=['POST'])
def nuovaTransazione():
    datiTransazione = request.get_json()
    #richiesta = ["nome"] # transazione dell'utente in formato json
    #richiesta = ["Nome", "Cognome", "IdDomande", "DomandeUscite", "RisposteSelezionate", "PunteggioDomande"]
    
    """if not all(k in datiTransazione for k in richiesta):
        return "Dati mancanti nella richiesta", 404"""

    datiTransazione["timestamp"] = time.time()
    blockchain.transazioniUnconfirmed.append(datiTransazione)# per aggiungere la transazione

    return "Transazione creata con successo", 201

#http://localhost:8000/mine 
# per comunicare al server di estrarre un nuovo blocco
@app.route('/mine', methods=['GET'])
def mineTransazioniUnconfirmed():
    block = blockchain.mine()
    ultimoBlocco = blockchain.chain[-1]
    if block is False:
        return "Nessuna transazione da estrarre", 404
    return "Il blocco {} è stato estratto.".format(ultimoBlocco.index)

# http://localhost:8000/pending 
# per verificare se ci sono altre transazioni non confermate
@app.route('/pending', methods=['GET'])
def getPending():
    transazioni = blockchain.transazioniUnconfirmed
    return json.dumps(transazioni), 200

#http://localhost:8000/chain 
# ci restituisce l’intera blockchain
@app.route('/chain', methods=['GET'])
def getChain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.__dict__)
    dimChain = len(chain)
    res = {"Lunghezza": dimChain, "Catena": chain}
    return json.dumps(res), 200

    
### manca la parte della decentralizzazione!! per inserire nuovi nodi nella rete.
if __name__ == '__main__':
    chainB = []

    app.run(port=8000)
    
    fileBC = open(r'C:\Users\ALESSIA9294\Desktop\ProgettoAPL\Progetto_APL\Python\d.pkl', 'wb')
    for block in blockchain.chain:
        chainB.append(block.__dict__)
    pickle.dump(chainB, fileBC)
    fileBC.close()
    
    with open('d.pkl', 'rb') as f:
        x = pickle.load(f)
        print("file pickle: ", x)
    
    #salva le transazioni in un file csv
    with open('bc.csv', 'w') as csvfile:
        for block in blockchain.chain:
            chainB.append(block.__dict__)
            
            dizion = block.transazioni
            #print("DSFSGDSFGDS:", block.nome)
            
            if len(dizion) > 0 :
                #print("CategorieDomande: ", block.transazioni["CategorieDomande"])
                print("TIPO : ", type(block.transazioni))
                print("KEYS: ", block.transazioni.keys())
                w = csv.DictWriter(csvfile,dizion.keys())
                w.writeheader() 
                w.writerow(dizion)

    
    

    
            
                #writer = csv.writer(csvfile, delimiter=',')
                #writer.writerow(chainB)