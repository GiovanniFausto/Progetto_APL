import json
import time
from flask import Flask, request
from Blockchain import Blockchain
import socket, ast
import requests


if __name__ == '__main__':
    #socketio.run(app, port=9999)  #Prova flask
    url = "http://localhost:8000/nuovaTransazione"
    url2 = "http://localhost:8000/mine"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    print("CLIENT ATTIVO")
    HOST = ''                 # Nome simbolico che rappresenta il nodo locale
    PORT = 9999              # Porta non privilegiata arbitraria 
    #prova
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.settimeout(1.0)
        s.listen(1)
        while 1:
            
            try:
                conn, addr = s.accept()
                print ('Connected by', addr)
                data = conn.recv(2048*4)
                datiRicevuti=data.decode("utf-8") # è una stringa
                if len(datiRicevuti)>2:
                    #print("-"*150)
                    res = json.loads(datiRicevuti) # trasforma in dizionario
                    json_str = json.dumps(res) #trasforma in json

                    #POST nuovaTransazione, mette la transazione nella lista transazioni non confermate
                    datiTransazione = requests.post(url, data=json_str, headers=headers)
                    print("Status code POST /nuovaTransazione: ", datiTransazione.status_code)

                    #GET mine, estrae le transazioni non confermate
                    transaction =requests.get(url2)
                    print("Status code GET /mine: ", transaction.status_code)
                          
            except socket.timeout: pass
            
    except KeyboardInterrupt: print("CLIENT SPENTO")
   
   

