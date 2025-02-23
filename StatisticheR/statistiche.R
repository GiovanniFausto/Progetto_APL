#Load RMariaDB if it is not loaded already
library(RMySQL)


user<-Sys.info()["user"]
if(user=="giova"){
  passwordMysql=""
} else {passwordMysql="0000"}

#prendo il data corrente
data<-Sys.Date()
giornoTest<-as.Date('2020-10-10')


if(data>giornoTest){# controllo se sono oltre un certo orario che significa che ho finito i test e quindi posso fare delle statistiche
  print("E' L'ORA GIUSTA PER FARE LE STATISTICHE")
 
  
  # serve per la connessione al db
  connessioneDB <- dbConnect(MySQL(), user="root", password=passwordMysql, host="localhost",db="apl")
  allTables <- dbListTables(connessioneDB)# mi ritorna la lista di tutte le tabelle nel db
  
  dfcandi <- dbReadTable(connessioneDB, "dfcandidato")#prendo le dataframe e tolgo la prima colonna che sono indici della tabella
  dftot <- dbReadTable(connessioneDB, "dftot")
  dbDisconnect(connessioneDB)# mi disconnetto una volta che ho preso le tabelle
  dfcandi<-dfcandi[-c(1)]#toglie gli indici dalla tabella che non serve
  dftot<-dftot[-c(1)]
  
  catefgorie<-names(dftot)# prendo nomi categorie e nomi candidati
  candidati<-dfcandi$candidato
  
  #contiene solo i punteggi di ogni categoria per il candidiato, in praitca rimuovo il nome dei candidati e le domande per categori
  categoriPunteggi<-dfcandi[-c(1:2)] #in pratica toglie i nomi e il numero di dom per categoria
  
  #sommo i punteggi delle colonne e che quindi sono i totali per ogni categoria
  sommaColonne<-colSums(dftot)
 
  numerdomande<-nrow(dftot)#contiene quante sono le domande totali di tutti i test per ogni determinata categoria, per fare una media generele
  numeroCategorie<-ncol(dftot)#sar 7 categorie
  numerdomcategoria<-dfcandi$domcat[[1]] #contiene il numero di domande per ogni categoria per ogni test, nel nosto caso 10
  
  #PLOT1------------------------------------------------------------------------------------------------------------------------------------------
  
  # sommo tutti i punteggi di una categoria e li divido per il numero di domande
  #ho qualcosa del tipo 10 punti su 40 domande esempio
  jpeg("../Plot/1_MediaPunteggiCategorieDomande.jpg", width = 800, height = 800)#serve per salvare le immagini
  par(mar=c(5, 13 ,4 ,2))
  barplot(sommaColonne/numerdomande, 
          beside=TRUE,las=2, names.arg =catefgorie, main="Risposte per ogni categoria", xlab="Punteggio", horiz=TRUE, col=rgb(0.2,0.4,0.6,0.6)) 
  dev.off()
  #PLOT2-----------------------------------------------------------------------------------------------------------------------------------------------
  
  #contiene una dataframe che ha i candidati e la somma dei loro punteggi del test, del tipo nome->totale
  output <- data.frame( candidati = dfcandi$candidato ,
                        punteggitotali = apply(dfcandi[3:9], 1, sum) )# da 3 a 9 ci sono le colonne coi punteggi
  #la ordino in modo che va dal punteggio pi? basso al pi? alto 
  output<-output[order(output$punteggitotali),]
  #la inverto cos? i primi sono quelli col punteggio pi? alto 
  output<-output[order(nrow(output):1),] 

  #questo invede ? per plottare i punteggi di ogni candidato, in pratica ? il suo punteggio finale del test
  
  jpeg("../Plot/2_PunteggiCandidati.jpg", width = 800, height = 800)
  
  #questo invede ? per plottare i punteggi di ogni candidato, in pratica ? il suo punteggio finale del test
  par(mar=c(5, 13 ,4 ,2))
  barplot(output$punteggitotali,
          beside=TRUE,las=2, names.arg = output$candidati, main="Punteggio di ogni candidato", xlab="Punteggio", horiz=TRUE, col=rgb(0.2,0.4,0.6,0.6))
  dev.off()
  #PLOT3-----------------------------------------------------------------------------------------------------------------------------------------------
  
  #un grafico semplice a torta simile al ptrimo 
  jpeg("../Plot/3_TortaCategorie.jpg", width = 800, height = 800)
  pie(sommaColonne/numerdomande, labels = catefgorie, main="Media punteggi")
  dev.off()
  
  #PLOT4-------------------------------------------------------------------------------------------------------------------------------------------------
  
  #creo una nuova dataframe che ha per indici i nomi dei candidati, mi serve per prendere il massimo e minimo, per colonne le categorie coi punteggi
  df1 <- data.frame(dfcandi[-c(1,2)], row.names = dfcandi$candidato)
  #faccio la trasposta cos? ho i candidati come colonne e quindi sommo le loro colonne per avere i punteggi massimo di ogni candidato
  sommaPuteggicandidati<-colSums(t(df1))
  #prendo il massimo e il minimo, considerando anche i nomi dei candidati che sono appunto i nomi delle colonne
  tiziobravo<-sommaPuteggicandidati[which.max(sommaPuteggicandidati)]
  tizioscarso<-sommaPuteggicandidati[which.min(sommaPuteggicandidati)]
  #metto massimo e min insieme per poi plottarli
  max_min<-c(tiziobravo,tizioscarso)
  #plotto max e min
  jpeg("../Plot/4_MiglirePeggiore.jpg", width = 800, height = 800)
  par(mar=c(5, 13 ,4 ,2))
  barplot(max_min,
          beside=TRUE,las=2, names.arg =names(max_min), main="Punteggio max e min", xlab="Punteggio", horiz=TRUE, col=rgb(0.2,0.4,0.6,0.6))
  dev.off()
  #PLOT5------------------------------------------------------------------------------------------------------------------------------------------------
  #punteggi ottenuti da tutti i tizi
  totPunteggi <- rowSums(categoriPunteggi)
  #numero partecipanti al test
  numeroTizi <- length(dfcandi$candidato)
  # somma del punteggio totale su tutti i tizi al test
  sommaPunteggio <-  sum(totPunteggi)
  #media punteggio totale
  media <- sommaPunteggio/numeroTizi
  #deviazione standard
  devstd <- sd(totPunteggi)
  
  #distribuzione normale
  y <- dnorm(totPunteggi, mean = media, sd = devstd)
  jpeg("../Plot/5_DistribuzionePunteggi.jpg", width = 800, height = 800)
  plot(totPunteggi,y, type="p", lwd= 5, main = "Distribuzione Normale")
  dev.off()
  #PLOT6------------------------------------------------------------------------------------------------------------------------------------------------
  
  #salva tutti i plot
  jpeg("../Plot/6_RiassuntoDati.jpg")
  
  par(mfrow = c(3,2), mar = c(4, 7, 3, 7))
  barplot(sommaColonne/numerdomande, 
          beside=TRUE,las=2, names.arg =catefgorie, main="Risposte per ogni categoria", xlab="Punteggio", horiz=TRUE, col=rgb(0.2,0.4,0.6,0.6)) 
  #punteggio primi 5 candidati
  output<-head(output, 5)
  barplot(output$punteggitotali,
          beside=TRUE,las=2, names.arg =output$candidati, main="Punteggio dei primi 5 candidati", xlab="Punteggio", horiz=TRUE, col=rgb(0.2,0.4,0.6,0.6))
  pie(colSums(dftot)/numerdomande, labels = catefgorie, main="Media punteggi")
  barplot(max_min,
          beside=TRUE,las=2, names.arg =names(max_min), main="Punteggio max e min", xlab="Punteggio", horiz=TRUE, col=rgb(0.2,0.4,0.6,0.6))
  plot(totPunteggi,y, main = "Distribuzione Normale")
  
  dev.off()
  
}else {
  print("non ? il momento giusto")
}