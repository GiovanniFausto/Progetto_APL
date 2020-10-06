package generatoreDomandeTest
import util.Random
import scala.collection.mutable._

class lettoreDomande(var path:String, var numDom:Int) {

  private val bufferedSource = io.Source.fromFile(path)//serve per leggere il file
  private var key = LinkedHashMap[String,String]()//serve per le key del file id categ ecc
  private var dict = LinkedHashMap[String,String]()//conterrà le risposte
  private var lista=List(LinkedHashMap[String,String]())//contiene tutto il file letto
  private var inizio = 0//serve per distinguere la prima riga del file
  private var set=SortedSet[String]()//serve per mettere le categorie senza doppioni
  private var set1=SortedSet[Int]()//serve per mettere i numeri random
  var listaDom=List(LinkedHashMap[String,String]()) //conterrà le domande del test
  elaboradomande()
  generaDomadeTest()


  private def generaDomadeTest():Unit={//genera le domande del test partendo da tutte le domande
    for (i<-1 until lista.length){
      var cat=(lista(i)("Categoria"))//metto le categorie nei set così so qunte categorie ho
      set+=cat
    }
    val Categ=(set.size) //num categorie
    val domPerCateg=((lista.length-1)/set.size) //domande per ogni categoria

    var j=0
    val h=domPerCateg

    while (j<Categ){
      while (set1.size<numDom){ //genero 10 numeri random perchè voglio 10 dom per categoria
        var x=(Random.nextInt(h)+1+h*j) //lo faccio fino a quando ho tutti numeri diversi
        set1+=x //i numeri sono generati prima da 1 a 100 poi 101 a 200 ecc
      }


      for (i<-0 until set1.size){ //converto il set in sequenza e con i numeri che ho nella seq prendo le domande
        val s=set1.toSeq
        val l=(lista(s(i)))
        listaDom = l :: listaDom //aggiungo le domande pescate nella lista domande
      }
      j+=1

      set1.clear()//pulisco il set così metto altri 10 numeri

    }
    listaDom=listaDom.reverse //le domande vengono inserite in modo lifo ma noi le voglioamo in oridne di inserimento
    listaDom=listaDom.drop(1) //tolgo il primo elemento che è vuoto

  }


  private def elaboradomande(): Unit = { //serve a leggere tutte le domande nel file
    for (line <- bufferedSource.getLines) {
      if (inizio == 0) { //controllo se sono alla prima riga
        val cols = line.replace("\"","").split(";").map(_.trim) //quello che leggo lo mentto nelle colonne
        val l = cols.length
        for (i <- 0 until  l ) {
          key += (cols(i)->"0")   //la prima riga contiene solo le key
        }
        inizio = inizio + 1
        lista=key::lista //le aggiungo alla lista
      }
      else {
        inizio = inizio + 1
        val cols = line.replace("\"","").split(";").map(_.trim) //come prima ma ora ci sono le domande
        val l = cols.length
        val s = key.keys.toSeq //prendo le key che mi servono per la mappa che sarà del tipo k->v
        for (i <- 0 until l ) {
          dict+= (s(i) -> cols(i)) //metto nella mappa
        }
        lista=dict.clone()::lista
      }
    }
    lista = lista.reverse
    lista = lista.drop(1)
    bufferedSource.close
  }

}
