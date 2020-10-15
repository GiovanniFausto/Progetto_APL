library(feather)
path1<-"../Save/dfcandidato.feather"
path2<-"../Save/dftot.feather"
h="ciao"

if (file.exists(path1) & file.exists(path2)){
  
  repeat{
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
  
  par(mfrow = c(2,2))#serve per poter plottare 4 grafici in 2x2
  
  # sommo tutti i punteggi di una categoria e li divido per il numero di domande
  #ho qualcosa del tipo 10 punti su 40 domande esempio
  barplot(as.matrix(sommaColonne/numerdomande), 
          beside=TRUE,las=2, names.arg =catefgorie, main="Risposte per ogni categoria",horiz=TRUE) 
  
  
  #questo invede è per plottare i punteggi di ogni candidato, in pratica è il suo punteggio finale del test
  barplot(as.matrix(rowSums(categoriPunteggi)),
          beside=TRUE,las=2, names.arg =candidati, main="Punteggio di ogni candidato",horiz=TRUE)
  
  
  #un grafico semplice a torta simile al ptrimo 
  pie(colSums(dftot)/numerdomande, labels = catefgorie, main="Media punteggi")
  
  #creo una nuova dataframe che ha per indici i nomi dei candidati, mi serve per prendere il massimo e minimo, per colonne le categorie
  df1 <- data.frame(dfcandi[-c(1,2)], row.names = dfcandi$candidato)
  #faccio la trasposta così ho i candidati come colonne e quindi sommo le loro colonne per avere i punteggi massimo di ogni candidato
  sommaPuteggicandidati<-colSums(t(df1))
  #prendo il massimo e il minimo, considerando anche i nomi dei candidati che sono appunto i nomi delle colonne
  tiziobravo<-sommaPuteggicandidati[which.max(sommaPuteggicandidati)]
  tizioscarso<-sommaPuteggicandidati[which.min(sommaPuteggicandidati)]
  #metto massimo e min insieme per poi plottarli
  max_min<-c(tiziobravo,tizioscarso)
  #plotto max e min
  barplot(as.matrix(max_min),
          beside=TRUE,las=2, names.arg =names(max_min), main="Punteggio di ogni candidato",horiz=TRUE)
  
  Sys.sleep(3.333)
  }
  break
}



