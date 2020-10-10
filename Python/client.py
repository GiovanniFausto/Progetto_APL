import json
import time
from flask import Flask, request
from Blockchain import Blockchain
#from flask_socketio import SocketIO
#from flask_restful import Api
import socket, ast
import requests


if __name__ == '__main__':
    #socketio.run(app, port=9999)  #Prova flask
    url = "http://localhost:8000/nuovaTransazione"
    url2 = "http://localhost:8000/mine"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    
    HOST = ''                 # Nome simbolico che rappresenta il nodo locale
    PORT = 9999              # Porta non privilegiata arbitraria 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print ('Connected by', addr)
    
    #while 1:
    data = conn.recv(2048)
    datiRicevuti=data.decode("utf-8") # è una stringa
    print("DATI RICEVUTI: ", datiRicevuti)
    res = json.loads(datiRicevuti) # trasforma in dizionario
    print("RES: ", res)
    json_str = json.dumps(res) #trasforma in json
    #conn.send(data)

    print("STRINGA JSON: ", json_str)
    #POST nuovaTransazione, mette la transazione nella lista transazioni non confermate
    datiTransazione = requests.post(url, data=json_str, headers=headers)
    print("Status code: ", datiTransazione.status_code)

    #GET mine, estrae le transazioni non confermate
    transaction =requests.get(url2)
    print("Status code: ", transaction.status_code)

    conn.close()

