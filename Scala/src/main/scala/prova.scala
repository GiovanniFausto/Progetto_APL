import generatoreDomandeTest.lettoreDomande

object Hello extends App {
  var path="src/main/scala/questionario.csv"
  var obj= new lettoreDomande(path=path)
  var lista=obj.listaDom
  println(lista)
  print(lista.length)

}