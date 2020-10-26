import json
import time
from Blockchain import Blockchain
import socket
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
        s.settimeout(5.0)
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
                    connesso=False
                    while connesso==False:
                        try:
                            datiTransazione = requests.post(url, data=json_str, headers=headers)
                            print("Status code POST /nuovaTransazione: ", datiTransazione.status_code)

                            #GET mine, estrae le transazioni non confermate
                            transaction =requests.get(url2)
                            print("Status code GET /mine: ", transaction.status_code)
                            connesso=True
                            #time.sleep(1)
                            conn.send("DATI INVIATI AL SERVER\n".encode())
                        except KeyboardInterrupt:
                            print("CLIENT SPENTO")
                            break
                        except :
                            print("SERVER NON ATTIVO")
                            connesso=False
                                      
            except socket.timeout: pass
            
    except KeyboardInterrupt: print("CLIENT SPENTO")
   
   

