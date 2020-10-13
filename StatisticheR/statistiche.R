library(feather)
path1<-"../Save/dfcandidato.feather"
path2<-"../Save/dftot.feather"
h="ciao"
repeat{
  if (file.exists(path1) & file.exists(path2)){
    dfcandi <- arrow::read_feather(path1)
    dftot <- arrow::read_feather(path2)
 
    print(dfcandi)
    print(dftot)
    
    
  }
  Sys.sleep(3.75)
  
}
