# Progetto_APL
Giovanni Fausto
Alessia Rondinella

## Blockchain per test
L'obiettivo di questo progetto è la creazione e gestione di test a risposta multipla, utilizzando la tecnologia blockchain.
L'immagine di seguito mostra la struttura del progetto e i linguaggi di programmazione utilizzati:

![alt text](https://github.com/GiovanniFausto/Progetto_APL/blob/master/IdeaProgetto.jpg)

In particolare, sono stati utilizzati:
- Scala: partendo da un file csv, contenente 700 domande che fanno riferimento a varie categorie, 
vengono generati casualmente dei test contenenti 70 domande a risposta multipla.
una volta generati questi test, viene gestita l'esecuzione vera e propria del test, in cui in particolare, 
è possibile scegliere due modalità di esecuzione del test:
  - Simulazione: modalità in cui viene chiesto all'utente il numero di test di cui effettuare una simulazione.
  - Svolgimento del test: modalità in cui l'utente partecipa attivamente al test, rispondendo alle varie domande.
In entrambe le modalità, si procede inserendo nome, congnome e codice del partecipante, e successivamente si procede
allo svolgimento del test, scegliendo per ogni domanda, una tra le possibili 4 opzioni.
Le risposte vengono valutate utilizzando il seguente criterio:
  - +1 per ogni risposta corretta;
  - -0.25 per ogni risposta errata;
  - 0 se non viene fornita una risposta;
Alla fine del test, i dati del partecipante ed il test, comprensivo delle domande uscite e punteggi ottenuti per ogni domanda, vengono
inviati al server py utilizzando le Socket.

- Python: Creazione della struttura tipica di una Blockchain e realizzazione di un server contenente gli endpoint per interagire con essa.
Il progetto è implementato su un'architettura RESTful, che utilizza il formato standard JSON per i messaggi per la comunicazione C/S.
In particolare, viene utilizzato il framework Flask per implementare le chiamate RESTful.
E' possibile utilizzare un Web client qualsiasi per interagire con gli endpoint RESTful, come Postman o curl.
Gli endpoint disponibili sono:
  - /nuovaTransazione - POST - per la creazione di una nuova transazione in un blocco;
  - /pending - GET - per verificare se ci sono altre transazioni non ancora confermate;
  - /mine - GET - per l'estrazione del nuovo blocco;
  - /chain - GET - permette di visualizzare l'intera blockchain.
Il server inoltre, esegue il salvataggio della bc, per poterla ricaricare in seguito, per non effettuare la creazione ogni volta.
Il salvataggio viene fatto utilizzando il modulo Pickle per la serializzazione della struttura dell'oggetto bc.
Vengono create delle dataframe bla bla mysql bla


- MySql: La persistenza è implementata attraverso un database MySql bla bla

- R: 

Vengono esposti i seguenti servizi su localhost:
- API REST in Py: http://localhost:8000
- MySql su Phpmyadmin bla bla

### Running Project
Le librerie che sono state utilizzate per il progetto sono: bla bla

Si procede come prima cosa ad avviare il server per istanziare la blockchain:
```
python serversql.py
```
successivamente ad avviare il client, per la ricezione socket:
```
python client.py
```
una volta avviati entrambi, è possibile fare partire il test in Scala:
```
palla palla
```
### Statistiche
![alt text](https://github.com/GiovanniFausto/Progetto_APL/blob/master/Plot/1_MediaPunteggiCategorieDomande.jpg)


![alt text](https://github.com/GiovanniFausto/Progetto_APL/blob/master/Plot/2_PunteggiCandidati.jpg)


![alt text](https://github.com/GiovanniFausto/Progetto_APL/blob/master/Plot/4_MiglirePeggiore.jpg)


![alt text](https://github.com/GiovanniFausto/Progetto_APL/blob/master/Plot/5_DistribuzionePunteggi.jpg)
