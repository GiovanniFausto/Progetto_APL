import json
import time
from flask import Flask, request
from Blockchain import Blockchain
#from flask_socketio import SocketIO
#from flask_restful import Api
import socket, ast

# creiamo delle interfacce per il nodo server.
# usiamo Flask come framework per creare un'applicazione REST
app = Flask(__name__)
#api = Api(app)
#socketio = SocketIO(app)

# copia della bc per il nodo server
blockchain = Blockchain()

#creiamo gli endpoint

#http://localhost:8000/nuovaTransazione 
# serve per creare una nuova transazione in un blocco
@app.route('/nuovaTransazione', methods=['POST'])
def nuovaTransazione():
    datiTransazione = request.get_json()
    richiesta = ["nome"] # transazione dell'utente in formato json

    for dati in richiesta:
        if not datiTransazione.get(dati):
            return "Dati mancanti", 404

    datiTransazione["timestamp"] = time.time()

    blockchain.aggiungiTransazione(datiTransazione) # per aggiungere la transazione

    return "Transazione creata con successo", 201

#http://localhost:8000/mine 
# per comunicare al server di estrarre un nuovo blocco
@app.route('/mine', methods=['GET'])
def mineTransazioniUnconfirmed():
    numeroBlocco = blockchain.mine()
    if numeroBlocco is False:
        return "Nessuna transazione da estrarre"
    return "Il blocco #{} è stato estratto.".format(numeroBlocco)

# http://localhost:8000/pending 
# per verificare se ci sono altre transazioni non confermate
@app.route('/pending')
def getPending():
    return json.dumps(blockchain.transazioniUnconfirmed)

#http://localhost:8000/chain 
# ci restituisce l’intera blockchain
@app.route('/chain', methods=['GET'])
def getChain():
    chain = []
    for block in blockchain.chain:
        chain.append(block)
    dimChain = len(chain)
    return json.dumps({"Lunghezza": dimChain,
                       "Catena": chain})

'''@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)'''
    
### manca la parte della decentralizzazione!! per inserire nuovi nodi nella rete.
if __name__ == '__main__':
    app.run(port=8000)
    #socketio.run(app, port=9999)  #Prova flask
    
    HOST = ''                 # Nome simbolico che rappresenta il nodo locale
    PORT = 9999              # Porta non privilegiata arbitraria 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print ('Connected by', addr)
    while 1:
        data = conn.recv(1024)
        prova=data.decode("utf-8")
        print(data.decode("utf-8"))
        if not data: 
            break
        conn.send(data)

    conn.close()

    print((prova))