library(feather)
path1<-"../Save/dfcandidato.feather"
path2<-"../Save/dftot.feather"
h="ciao"

if (file.exists(path1) & file.exists(path2)){
  dfcandi <- arrow::read_feather(path1)
  dftot <- arrow::read_feather(path2)
  catefgorie<-names(dftot)
  candidati<-dfcandi$candidato
  print(candidati)
  prova<-dfcandi[-c(1:2)]
  print("----------------------tabella candidati----------------------------------------------")
  print(prova)
  print("----------------------tabella totali----------------------------------------------")
  print(dftot)
  
  sommaColonne<-colSums(dftot)
  
  
  numerdomande<-nrow(dftot)
  numeroCategorie<-ncol(dftot)#sarà 7 categorie
  numerdomcategoria<-dfcandi$domcat[[1]] #contiene il numero di domande per ogni categoria
  # sommo tutti i punteggi di una categoria e li divido per il numero di domande
  #ho qualcosa del tipo 10 punti su 40 domande esempio
  barplot(as.matrix(colSums(dftot)/numerdomande), 
          beside=TRUE, names.arg =catefgorie, main="Risposte per ogni categoria") 
  
  Sys.sleep(5)
  
  barplot(as.matrix(rowSums(prova)/(numeroCategorie*numerdomcategoria)),
          beside=TRUE, names.arg =candidati, main="Punteggio di ogni candidato") 
  
}

  

