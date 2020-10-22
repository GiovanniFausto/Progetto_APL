import json
import pyarrow.feather as feather
import time
from flask import Flask, request
from Blockchain import Blockchain
import csv
import pandas as pd
import pickle
from os import path as P
from collections import defaultdict
from pathlib import Path

import sqlalchemy
#faccio quello che serve per connettermi al db creato 
sqlEngine       = sqlalchemy.create_engine('mysql+pymysql://root:0000@127.0.0.1/apl', pool_recycle=3600)
dbConnection    = sqlEngine.connect()
# creiamo delle interfacce per il nodo server.
# usiamo Flask come framework per creare un'applicazione REST

app = Flask(__name__)

#path
path=Path("..\BC\Blockchain.pkl")


#creo le dataframe per poi usarle in R
dataframeTot=defaultdict(list)
dataframeCandidato=defaultdict(list)

def calcolaInfoDomande():
    lenCatdom=len(blockchain.chain[1].categorieDomande)#saranno 7 
    lenPunt=len(blockchain.chain[1].punteggioDomande)
    numPunDom=int(lenPunt/lenCatdom) #ho in pratica quante domande per categoria
    return lenCatdom,lenPunt,numPunDom
    
#controllo se esiste già una bc, e in caso carico quella
if P.exists(path):
    print("bc esistente")
    with open(path, 'rb') as f:
        blockchain = pickle.load(f)   

    #lenCatdom=len(blockchain.chain[1].categorieDomande)#saranno 7 
    #lenPunt=len(blockchain.chain[1].punteggioDomande)
    #numPunDom=int(lenPunt/lenCatdom) #ho in pratica quante domande per categoria

    lenCatdom,lenPunt,numPunDom=calcolaInfoDomande()

    for block in blockchain.chain:#scorro i blocchi di bc
        if block.index==0:pass #salto il primo che non mi serve
        else:
            puntDom=block.punteggioDomande #è una lsita coi punteggi 
            dataframeCandidato["candidato"].append(block.infoCandidato())
            dataframeCandidato["domcat"].append(numPunDom)
            for i,k in enumerate(block.categorieDomande): #scorro le categorie 
                sliceDom=puntDom[numPunDom*i:numPunDom*i+numPunDom] #prendo uno slice che sarebbero solo le domande di quella categoria
                dataframeCandidato[k].append(sum(sliceDom)) #sommo il punteggio di quelle domande
                for ele in sliceDom:
                    dataframeTot[k].append(ele)

            dftot = pd.DataFrame(data=dataframeTot) #le convero in dataframe pandas per salvarle poi in feather
            dfcandidato = pd.DataFrame(data=dataframeCandidato)

    frame = dfcandidato.to_sql("dfcandidato", dbConnection,if_exists='replace')
    frame = dftot.to_sql("dftot", dbConnection,if_exists='replace')
    #blockchain.stampa()
else:
    print("bc no presente")
    blockchain = Blockchain()
    #blockchain.stampa()



#salva la bc in un file Pickle
def saveBCOnPickle():
    fileBC = open(path, 'wb')
    pickle.dump(blockchain, fileBC)
    fileBC.close()

#salva i punteggi in dataframe, per R
def salvaDataframe(block):     
    lenCatdom,lenPunt,numPunDom=calcolaInfoDomande()
    
    puntDom=block.punteggioDomande #è una lsita coi punteggi 
    dataframeCandidato["candidato"].append(block.infoCandidato())
    dataframeCandidato["domcat"].append(numPunDom)
    for i,k in enumerate(block.categorieDomande): #scorro le categorie 
        sliceDom=puntDom[numPunDom*i:numPunDom*i+numPunDom] #prendo uno slice che sarebbero solo le domande di quella categoria
        dataframeCandidato[k].append(sum(sliceDom)) #sommo il punteggio di quelle domande
        for ele in sliceDom:
            dataframeTot[k].append(ele)
    
    dftot = pd.DataFrame(data=dataframeTot) #le convero in dataframe pandas per salvarle poi in feather
    dfcandidato = pd.DataFrame(data=dataframeCandidato)

    frame = dfcandidato.to_sql("dfcandidato", dbConnection,if_exists='replace')
    frame = dftot.to_sql("dftot", dbConnection,if_exists='replace')

#creiamo gli endpoint

#http://localhost:8000/nuovaTransazione ---------------------------------------------------------------------- NUOVA TRANSIZIONE
# serve per creare una nuova transazione in un blocco
@app.route('/nuovaTransazione', methods=['POST'])
def nuovaTransazione():
    datiTransazione = request.get_json() # richiesta in formato json
    datiTransazione["timestamp"] = time.time() #mette il timestamp alla transaz
    blockchain.transazioniUnconfirmed.append(datiTransazione)# per aggiungere la transazione alla lista di transaz non confermate
    return "Transazione creata con successo", 201 

#http://localhost:8000/mine ----------------------------------------------------------------------  MINE
# per comunicare al server di estrarre un nuovo blocco
@app.route('/mine', methods=['GET'])
def mineTransazioniUnconfirmed():
    block = blockchain.mine() # mine delle transazioni non confermate
    ultimoBlocco = blockchain.chain[-1] #prende l'ultimo blocco appena aggiutno
    if block is False:
        return "Nessuna transazione da estrarre", 404
    #questo salva la bc
    saveBCOnPickle()
    #salva dataframe
    salvaDataframe(ultimoBlocco)

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
    chain = blockchain.getChain() # prende tutta la bc
    dimChain = len(chain)
    res = {"Lunghezza": dimChain, "Catena": chain}
    return json.dumps(res), 200 #restituisce in formato json la bc

@app.route('/partecipanti', methods=['GET'])    
def getPartecipantiTest():
    partecipanti = []
    for block in blockchain.chain:
        if block.index > 0: 
            tot = sum(block.punteggioDomande)
            partecipanti.extend([block.infoCandidato(), tot])
    return json.dumps(partecipanti), 200

### manca la parte della decentralizzazione!! per inserire nuovi nodi nella rete.
if __name__ == '__main__': #----------------------------------------------------------------------------- MAIN
    print("SERVER ATTIVO")
    app.run(port=8000)
    print("SERVER SPENTO")
