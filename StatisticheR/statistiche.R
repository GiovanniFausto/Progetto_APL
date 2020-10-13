library(feather)
path1<-"../Save/dfcandidato.feather"
path2<-"../Save/dftot.feather"
h="ciao"

if (file.exists(path1) & file.exists(path2)){
  dfcandi <- arrow::read_feather(path1)
  dftot <- arrow::read_feather(path2)
  
  print("----------------------tabella candidati----------------------------------------------")
  print(dfcandi)
  print("----------------------tabella totali----------------------------------------------")
  print(dftot)
  #print(colSums(dfcandi[,(-1:-2)])) #prende tutto tranne la prima colonna
  
  
}

  

