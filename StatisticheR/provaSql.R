#Load RMariaDB if it is not loaded already
library(RMySQL)
library(lubridate)

ora<-Sys.time()#prendo il tempo corrente e poi prendo ore e minuti
ore<-hour(ora)
minuti<-minute(ora)
oraCorrente<-paste(ore, minuti,sep=":")

target <- "10:00"#quello da confontare 

if(oraCorrente>target){# controllo se sono oltre un certo orario che significa che ho finito i test e quindi posso fare delle statistiche
  print("E' L'ORA GIUSTA PER FARE LE STATISTICHE")
  ucscDb <- dbConnect(MySQL(), user="root", password="", host="localhost",db="apl")# serve per la connessione al db
  
  allTables <- dbListTables(ucscDb)# mi ritorna la lista di tutte le tabelle nel db
  
  dfcandi <- dbReadTable(ucscDb, "dfcandidato")#prendo le dataframe e tolgo la prima colonna che sono indici della tabella
  dftot <- dbReadTable(ucscDb, "dftot")
  dfcandi<-dfcandi[-c(1)]
  dftot<-dftot[-c(1)]
  
  catefgorie<-names(dftot)# prendo nomi categorie e nomi candidati
  candidati<-dfcandi$candidato
  
  #contiene solo i punteggi di ogni categoria per il candidiato, in praitca rimuovo il nome dei candidati e le domande per categori
  categoriPunteggi<-dfcandi[-c(1:2)]
  #sommo i punteggi delle colonne e che quindi sono i totali per ogni categoria
  sommaColonne<-colSums(dftot)
  
  
  numerdomande<-nrow(dftot)#contiene quante sono le domande totali di tutti i test per ogni determinata categoria, per fare una media generele
  numeroCategorie<-ncol(dftot)#sar 7 categorie
  numerdomcategoria<-dfcandi$domcat[[1]] #contiene il numero di domande per ogni categoria
  
  
  #par(mfrow = c(3,2), mar = c(4, 7, 3, 7))#serve per poter plottare 4 grafici in 2x2 [mar = c(bottom, left, top, right)]
  
  #-------------------------------------------------------------------------------------------------------------------------------------------------------
  
  # sommo tutti i punteggi di una categoria e li divido per il numero di domande
  #ho qualcosa del tipo 10 punti su 40 domande esempio
  jpeg("image/plot1.jpg", width = 800, height = 800)#serve per salvare le immagini
  par(mar=c(5, 13 ,4 ,2))
  barplot(as.matrix(sommaColonne/numerdomande), 
          beside=TRUE,las=2, names.arg =catefgorie, main="Risposte per ogni categoria", xlab="Punteggio", horiz=TRUE) 
  dev.off()
  #-------------------------------------------------------------------------------------------------------------------------------------------------------
  
  #contiene una dataframe che ha i candidati e la somma dei loro punteggi del test
  output <- data.frame( candidati = dfcandi$candidato ,
                        punteggitotali = apply(dfcandi[3:9], 1, sum) )
  #la ordino in modo che va dal punteggio pi? basso al pi? alto 
  output<-output[order(output$punteggitotali),]
  #la inverto cos? i primi sono quelli col punteggio pi? alto 
  output<-output[order(nrow(output):1),] 

  #questo invede ? per plottare i punteggi di ogni candidato, in pratica ? il suo punteggio finale del test
  
  jpeg("image/plot2.jpg", width = 800, height = 800)
  #output<-head(output,10) per prendere i primi 10
  
  #questo invede ? per plottare i punteggi di ogni candidato, in pratica ? il suo punteggio finale del test
  par(mar=c(5, 13 ,4 ,2))
  barplot(output$punteggitotali,
          beside=TRUE,las=2, names.arg = output$candidati, main="Punteggio di ogni candidato", xlab="Punteggio", horiz=TRUE)
  dev.off()
  #-------------------------------------------------------------------------------------------------------------------------------------------------------
  
  #un grafico semplice a torta simile al ptrimo 
  jpeg("image/plot3.jpg", width = 800, height = 800)
  pie(colSums(dftot)/numerdomande, labels = catefgorie, main="Media punteggi")
  dev.off()
  
  #-------------------------------------------------------------------------------------------------------------------------------------------------------
  
  #creo una nuova dataframe che ha per indici i nomi dei candidati, mi serve per prendere il massimo e minimo, per colonne le categorie
  df1 <- data.frame(dfcandi[-c(1,2)], row.names = dfcandi$candidato)
  #faccio la trasposta cos? ho i candidati come colonne e quindi sommo le loro colonne per avere i punteggi massimo di ogni candidato
  sommaPuteggicandidati<-colSums(t(df1))
  #prendo il massimo e il minimo, considerando anche i nomi dei candidati che sono appunto i nomi delle colonne
  tiziobravo<-sommaPuteggicandidati[which.max(sommaPuteggicandidati)]
  tizioscarso<-sommaPuteggicandidati[which.min(sommaPuteggicandidati)]
  #metto massimo e min insieme per poi plottarli
  max_min<-c(tiziobravo,tizioscarso)
  #plotto max e min
  jpeg("image/plot4.jpg", width = 800, height = 800)
  par(mar=c(5, 13 ,4 ,2))
  barplot(as.matrix(max_min),
          beside=TRUE,las=2, names.arg =names(max_min), main="Punteggio di ogni candidato", xlab="Punteggio", horiz=TRUE)
  dev.off()
  #-------------------------------------------------------------------------------------------------------------------------------------------------------
  #punteggi ottenuti da tutti i tizi
  totPunteggi <- rowSums(categoriPunteggi)
  #numero partecipanti al test
  numeroTizi <- length(dfcandi$candidato)
  # somma del punteggio totale tu tutti i tizi al test
  sommaPunteggio <-  sum(totPunteggi)
  
  #media punteggio totale
  media <- sommaPunteggio/numeroTizi
  #deviazione standard
  devstd <- sd(totPunteggi)
  
  #distribuzione normale
  y <- dnorm(totPunteggi, mean = media, sd = devstd)
  jpeg("image/plot5.jpg", width = 800, height = 800)
  plot(totPunteggi,y, type="p", lwd= 5, main = "Distribuzione Normale")
  dev.off()
  #-------------------------------------------------------------------------------------------------------------------------------------------------------
  
  #salva tutti i plot
  jpeg("image/rdata.jpg")
  par(mfrow = c(3,2), mar = c(4, 7, 3, 7))
  barplot(as.matrix(sommaColonne/numerdomande), 
          beside=TRUE,las=2, names.arg =catefgorie, main="Risposte per ogni categoria", xlab="Punteggio", horiz=TRUE) 
  #punteggio primi 5 candidati
  output<-head(output, 5)
  barplot(output$punteggitotali,
          beside=TRUE,las=2, names.arg =output$candidati, main="Punteggio dei primi 5 candidati", xlab="Punteggio", horiz=TRUE)
  pie(colSums(dftot)/numerdomande, labels = catefgorie, main="Media punteggi")
  barplot(as.matrix(max_min),
          beside=TRUE,las=2, names.arg =names(max_min), main="Punteggio di ogni candidato", xlab="Punteggio", horiz=TRUE)
  plot(totPunteggi,y, main = "Distribuzione Normale")
  
  dev.off()
  
  
}