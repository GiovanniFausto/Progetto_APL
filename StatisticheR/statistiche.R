library(feather)

path1<-"../Save/dfcandidato.feather"
path2<-"../Save/dftot.feather"
h="ciao"

if (file.exists(path1) & file.exists(path2)){
  
  #repeat{
  #contengono le dataframe salvate da py
  dfcandi <- arrow::read_feather(path1)
  dftot <- arrow::read_feather(path2)
  #contengono le categorie e i nomi dei candidati
  catefgorie<-names(dftot)
  candidati<-dfcandi$candidato
  #contiene solo i punteggi di ogni categoria per il candidiato 
  categoriPunteggi<-dfcandi[-c(1:2)]
  #sommo i punteggi delle colonne e che quindi sono i totali per ogni categoria
  sommaColonne<-colSums(dftot)
  
  
  numerdomande<-nrow(dftot)#contiene quante sono le domande totali di tutti i test per ogni determinata categoria, per fare una media generele
  numeroCategorie<-ncol(dftot)#sar 7 categorie
  numerdomcategoria<-dfcandi$domcat[[1]] #contiene il numero di domande per ogni categoria
  
  par(mfrow = c(3,2), mar = c(4, 7, 3, 7))#serve per poter plottare 4 grafici in 2x2 [mar = c(bottom, left, top, right)]
  
  #------------------------------------------------------------------------------------------------------------
  
  # sommo tutti i punteggi di una categoria e li divido per il numero di domande
  #ho qualcosa del tipo 10 punti su 40 domande esempio
  barplot(as.matrix(sommaColonne/numerdomande), 
          beside=TRUE,las=2, names.arg =catefgorie, main="Risposte per ogni categoria", xlab="Punteggio", horiz=TRUE) 
  
  #------------------------------------------------------------------------------------------------------------
  #contiene una dataframe che ha i candidati e la somma dei loro punteggi del test
  output <- data.frame( candidati = dfcandi$candidato ,
                        punteggitotali = apply(dfcandi[3:9], 1, sum) )
  #la ordino in modo che va dal punteggio più basso al più alto 
  output<-output[order(output$punteggitotali),]
  #la inverto così i primi sono quelli col punteggio più alto 
  output<-output[order(nrow(output):1),] 

  #questo invede ? per plottare i punteggi di ogni candidato, in pratica ? il suo punteggio finale del test
  barplot(output$punteggitotali,
          beside=TRUE,las=2, names.arg =output$candidati, main="Punteggio di ogni candidato", xlab="Punteggio", horiz=TRUE)
  
  #------------------------------------------------------------------------------------------------------------
  
  #un grafico semplice a torta simile al ptrimo 
  pie(colSums(dftot)/numerdomande, labels = catefgorie, main="Media punteggi")
  
  #------------------------------------------------------------------------------------------------------------
  
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
  barplot(as.matrix(max_min),
          beside=TRUE,las=2, names.arg =names(max_min), main="Punteggio di ogni candidato", xlab="Punteggio", horiz=TRUE)
  
  #------------------------------------------------------------------------------------------------------------
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
  plot(totPunteggi,y, main = "Distribuzione Normale",)
  
  Sys.sleep(3.333)
  #}
  #break
}



