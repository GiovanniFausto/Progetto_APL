import json
import time
from flask import render_template, Flask, request
from Blockchain import Blockchain
import pandas as pd
import pickle
import os
from os import path as P
from collections import defaultdict
from pathlib import Path
import sqlalchemy
import datetime

pc=os.environ['COMPUTERNAME']
password="" if pc=="DESKTOP-LOU6DAQ" else "0000"
urlMysql='mysql+pymysql://root:'+password+'@127.0.0.1'
nomedb="apl"
try:
    #faccio quello che serve per connettermi al db creato 
    sqlEngine       = sqlalchemy.create_engine(urlMysql) 
    dbConnection = sqlEngine.execute("CREATE DATABASE IF NOT EXISTS "+nomedb) #create db
    sqlEngine       = sqlalchemy.create_engine(urlMysql+"/"+nomedb)
    #dbConnection = sqlEngine.execute("USE apl;") # select new db
    dbConnection    = sqlEngine.connect()
#except ConnectionRefusedError:
    #print("ERRORE CONNESSIONE DB")
except sqlalchemy.exc.OperationalError:
    print("ERRORE CONNESSIONE DB")


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
    lenPunt=len(blockchain.chain[1].punteggioDomande)# ci sono tutti i punteggi, quindi se ho 7 categorie e di ogniuna 10 domande avrò 70 valori
    numPunDom=int(lenPunt/lenCatdom) #ho in pratica quante domande per categoria
    return lenCatdom,lenPunt,numPunDom
    
#controllo se esiste già una bc, e in caso carico quella
if P.exists(path):
    print("bc esistente")
    with open(path, 'rb') as f:
        blockchain = pickle.load(f)   
    
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

            dftot = pd.DataFrame(data=dataframeTot) #le convero in dataframe pandas
            dfcandidato = pd.DataFrame(data=dataframeCandidato)
    try:
        frame = dfcandidato.to_sql("dfcandidato", dbConnection, if_exists='replace')# la prima volta facciamo un replace, non si sa mai c'è qualche problema col db
        frame = dftot.to_sql("dftot", dbConnection, if_exists='replace')# così abbiamo ricreato tutta la tabella e la carichiamo
    except NameError:
        print("Errore connessione Database")

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
    dataframeCandidato["candidato"].append(block.infoCandidato())# mettiamo le info del candicato nome cognome codice
    dataframeCandidato["domcat"].append(numPunDom)# quante domande ho per ogni categoria
    for i,k in enumerate(block.categorieDomande): #scorro le categorie 
        sliceDom=puntDom[numPunDom*i:numPunDom*i+numPunDom] #prendo uno slice che sarebbero solo le domande di quella categoria
        dataframeCandidato[k].append(sum(sliceDom)) #sommo il punteggio di quelle domande
        for ele in sliceDom:
            dataframeTot[k].append(ele)# qui inceve appendo i punteggi che ci sono in ogni slice, per averli tutti sulla colonna della categoria k
    
    dftot = pd.DataFrame(data=dataframeTot) #le convero in dataframe pandas 
    dfcandidato = pd.DataFrame(data=dataframeCandidato)
    try:
        frame = dfcandidato.tail(1).to_sql("dfcandidato", dbConnection,if_exists='append')# devo aggiungere solo l'ultimo
        frame = dftot.tail(numPunDom).to_sql("dftot", dbConnection,if_exists='append')# devo aggingere le ultime domande 
    except NameError:
        print("Errore connessione Database")
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

@app.route('/partecipanti/<codice>', methods=['GET'])    
def getPartecipantexTest(codice):
    partecipantex = []
    for block in blockchain.chain:
        if block.index > 0 and block.codice == codice: 
            partecipantex.append(block.transazioni)
    return json.dumps(partecipantex), 200

CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"
@app.route('/')
def index():
    #fetch_posts()
    return render_template('index.html',
                           title='Blockchain',
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)

def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')


if __name__ == '__main__': #----------------------------------------------------------------------------- MAIN
    print("SERVER ATTIVO")
    app.run(port=8000)
    print("SERVER SPENTO")
