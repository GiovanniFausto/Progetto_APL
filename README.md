# Progetto_APL
Giovanni Fausto
Alessia Rondinella

## Blockchain per test
L'obiettivo di questo progetto è la creazione e gestione di test a risposta multipla, utilizzando la tecnologia blockchain.

L'immagine di seguito mostra la struttura del progetto e i linguaggi di programmazione utilizzati:

![alt text](https://github.com/GiovanniFausto/Progetto_APL/blob/master/IdeaProgetto.jpg)

In particolare, sono stati utilizzati:

## Scala:

Partendo da un file csv, contenente 700 domande che fanno riferimento a 7  categorie diverse, vengono generati casualmente dei test contenenti 70 domande a risposta multipla.
Una volta generati questi test, viene gestita l'esecuzione vera e propria del test, in cui in particolare, è possibile scegliere due modalità di esecuzione del test:
  - Simulazione: modalità in cui viene chiesto all'utente il numero di test di cui effettuare una simulazione.
  - Svolgimento del test: modalità in cui l'utente partecipa attivamente al test, rispondendo alle varie domande.

In entrambe le modalità, si procede inserendo nome, cognome e codice del partecipante, e successivamente si procede allo svolgimento del test, scegliendo per ogni domanda, una tra le possibili 4 opzioni, prese anch'esse dal file cvs e sono mescolate tra di loro perchè altrimento la prima risposta sarebbe sempre quella corretta.

Le risposte vengono valutate utilizzando il seguente criterio:
  - +1 per ogni risposta corretta;
  - 0 per ogni risposta errata;
  - +0.25 se non viene fornita una risposta;

Alla fine del test, i dati del partecipante ed il test, comprensivo delle domande uscite e punteggi ottenuti per ogni domanda, vengono
inviati al client py utilizzando le Socket.

## Python: 

Creazione della struttura Blockchain e realizzazione di un server contenente gli endpoint per interagire con essa.
Il progetto è implementato su un'architettura RESTful, che utilizza il formato standard JSON per i messaggi per la comunicazione C/S.
In particolare, viene utilizzato il framework Flask per implementare le chiamate RESTful.
E' possibile utilizzare un Web client qualsiasi per interagire con gli endpoint RESTful, come Postman o curl.
Gli endpoint disponibili sono:
  - /nuovaTransazione - POST - per la creazione di una nuova transazione in un blocco;
  - /pending - GET - per verificare se ci sono altre transazioni non ancora confermate;
  - /mine - GET - per l'estrazione del nuovo blocco;
  - /chain - GET - permette di visualizzare l'intera blockchain;
  - /partecipanti - GET - restituisce l'elenco dei partecipanti al test e il punteggio totale ottenuto da ognuno.

Il server inoltre, esegue il salvataggio della bc, per poterla ricaricare in seguito, per non effettuare la creazione ogni volta.
Il salvataggio viene fatto utilizzando il modulo Pickle per la serializzazione della struttura dell'oggetto bc.

Viene realizzato un client per la ricezione Socket del test effettuato, si occupa successivamente di effettuare la richiesta GET di creazione della transazione da inserire in BC e la richiesta POST per effettuare il mine del blocco.
Ogni volta che viene aggiunto un novo blocco, e quindi che viene fatto il mine, viene aggiunto un nuovo valore anche alla dataframe, questa a sua volta viene salvata su un DataBase MYSql sotto forma di tabella, in modo tale che sia poi semplice usare questi dati per fare delle statistiche su R.


## MySql: 

La persistenza dei dati è implementata attraverso un database MySql, a tal fine viene creato un database apl, che conterrà due tabelle.
## R:
Le statistiche sono state implementate in R in quanto è il più portato dei tre linguaggi per questo tipo di operazioni. 

In particolare abbiamo pensato di calcolare 5 differenti statistiche:
- La media dei punteggi relativi alle varie categorie, principalmente per capire qualche categoria è andata peggio o meglio, e quindi in futuro andare a cambiare la tipologia di domande;
- I punteggi totali di ogni candidato, andando a metterli in ordine decrescente in modo tale da rendersi subito conto di chi ha fatto un punteggio più alto;
- Abbiamo anche riportato la media dei punteggi delle categorie su un grafico a torta in modo tale da renderlo più comprensibile;
- I punteggi del peggiore e migliore candidato;
- La distribuzione dei punteggi, per capire in media come sono andati i test;
- Infine un grafico riassuntivo dei precedenti.

Di seguito sono presenti delle immagini relativa alle statistiche che abbiamo ottenuto.

Vengono esposti i seguenti servizi su localhost:
- API REST in Py: http://localhost:8000
- MySql anch'esso su localhost 

## Running Project

Le librerie che sono state utilizzate per il progetto sono: 

- Per quanto riguarda la parte di Scala quelle standard presenti già su Scala.
- Per R abbiamo usato RMySQL che serve per la connessione al db, e lubridate che serve per fare delle operazioni con le date, per il resto abbiamo usato quelle standard di R
- Per Python hashlib per generare gli hash per i vari blocchi della blockchian, json e flask per le operazioni tra C/S


Si procede come prima cosa ad avviare il server per istanziare la blockchain
```
python serversql.py
```
Successivamente ad avviare il client, per la ricezione socket:
```
python client.py
```
una volta avviati entrambi, è possibile fare partire il test in Scala:

## Statistiche
![alt text](https://github.com/GiovanniFausto/Progetto_APL/blob/master/Plot/1_MediaPunteggiCategorieDomande.jpg)


![alt text](https://github.com/GiovanniFausto/Progetto_APL/blob/master/Plot/2_PunteggiCandidati.jpg)


![alt text](https://github.com/GiovanniFausto/Progetto_APL/blob/master/Plot/4_MiglirePeggiore.jpg)


![alt text](https://github.com/GiovanniFausto/Progetto_APL/blob/master/Plot/5_DistribuzionePunteggi.jpg)
