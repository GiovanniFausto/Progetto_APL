import json
import pyarrow.feather as feather
import time
from flask import Flask, request
from Blockchain import Blockchain
import csv
import pandas as pd
import pickle
#import torch
import os
from os import path as P
from collections import defaultdict
from pathlib import Path

# creiamo delle interfacce per il nodo server.
# usiamo Flask come framework per creare un'applicazione REST
app = Flask(__name__)
# copia della bc per il nodo server

path=Path("Save\Blockchain.pkl")
pathSave="Save"
#controllo se esiste già una bc, e in caso carico quella
if P.exists(path):
    print("bc esistente")
    with open(path, 'rb') as f:
        blockchain = pickle.load(f)   
    blockchain.stampa()
else:
    print("bc no presente")
    blockchain = Blockchain()
    #blockchain.stampa()

#creiamo gli endpoint

#http://localhost:8000/nuovaTransazione ---------------------------------------------------------------------- NUOVA TRANSIZIONE
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

#http://localhost:8000/mine ----------------------------------------------------------------------  MINE
# per comunicare al server di estrarre un nuovo blocco
@app.route('/mine', methods=['GET'])
def mineTransazioniUnconfirmed():
    block = blockchain.mine()
    ultimoBlocco = blockchain.chain[-1]
    
    if block is False:
        return "Nessuna transazione da estrarre", 404
    #questo salva la bc
    salva()
    return "Il blocco {} è stato estratto.".format(ultimoBlocco.index)

# http://localhost:8000/pending ---------------------------------------------------------------------- PENDING
# per verificare se ci sono altre transazioni non confermate
@app.route('/pending', methods=['GET'])
def getPending():
    transazioni = blockchain.transazioniUnconfirmed
    return json.dumps(transazioni), 200

#http://localhost:8000/chain ---------------------------------------------------------------------- CHAIN
# ci restituisce l’intera blockchain
@app.route('/chain', methods=['GET'])
def getChain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.__dict__)
    dimChain = len(chain)
    res = {"Lunghezza": dimChain, "Catena": chain}
    return json.dumps(res), 200

def salva():
    #salva la bc su un file
    fileBC = open(path, 'wb')
    pickle.dump(blockchain, fileBC)
    fileBC.close()
    #creo le dataframe per poi usarle in R
    dataframeTot=defaultdict(list)
    dataframeCandidato=defaultdict(list)
    lenCatdom=len(blockchain.chain[1].categorieDomande)#saranno 7 
    lenPunt=len(blockchain.chain[1].punteggioDomande)
    numPunDom=int(lenPunt/lenCatdom) #ho in pratica quante domande per categoria

    for block in blockchain.chain:#scorro i blocchi di bc
        if block.index==0:pass #salto il primo che non mi serve
        else:
            puntDom=block.punteggioDomande #è una lsita coi punteggi 
            dataframeCandidato["candidato"].append(block.nome+block.cognome+block.codice)
            for i,k in enumerate(block.categorieDomande): #scorro le categorie 
                sliceDom=puntDom[numPunDom*i:numPunDom*i+numPunDom] #prendo uno slice che sarebbero solo le domande di quella categoria
                dataframeCandidato[k].append(sum(sliceDom)) #sommo il punteggio di quelle domande
                for ele in sliceDom:
                    #dataframe["candidato"].append((block.nome+block.cognome))1
                    dataframeTot[k].append(ele)
    
    dftot = pd.DataFrame(data=dataframeTot) #le convero in dataframe pandas per salvarle poi in feather
    dfcandidato = pd.DataFrame(data=dataframeCandidato)
    feather.write_feather(dftot,pathSave + '\dftot.feather')
    feather.write_feather(dfcandidato,pathSave + '\dfcandidato.feather')
    
### manca la parte della decentralizzazione!! per inserire nuovi nodi nella rete.
if __name__ == '__main__': #----------------------------------------------------------------------------- MAIN
    chainB = []

    app.run(port=8000)
    print("fine")
