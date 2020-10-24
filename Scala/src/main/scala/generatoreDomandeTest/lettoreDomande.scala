package generatoreDomandeTest
import util.Random
import scala.collection.mutable._

class lettoreDomande(var path:String, var numDom:Int) {

  private val bufferedSource = io.Source.fromFile(path)//serve per leggere il file
  private var key = LinkedHashMap[String,String]()//serve per le key del file id categ ecc
  private var dict = LinkedHashMap[String,String]()//conterrà le risposte
  private var lista=List(LinkedHashMap[String,String]())//contiene tutto il file letto, è una lista di hashmap
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
    val Categ=(set.size) //num categorie sono 7
    val domPerCateg=((lista.length-1)/set.size) //domande per ogni categoria se la lista è lunga 700 ho 100 dom per ogni cat, di queste
                                                // ne prendo un sotto insieme
    var j=0
    val h=domPerCateg //serve per poi generare i numeri random e saltare da una categoria all'altra

    while (j<Categ){ //lo faccio per ogni categoria
      while (set1.size<numDom){ //genero tot numeri random perchè voglio tot dom per categoria
        var x=(Random.nextInt(h)+1+h*j) //lo faccio fino a quando ho tutti numeri diversi, anche perchè è un set
        set1+=x //i numeri sono generati prima da 1 a 100 poi 101 a 200 ecc
        //Random.nextInt(h) genera un random da 0 a 99 con +1 faccio da 1 a 100 perchè tanto la prima riga sono info
        //+h*j serve per saltare di 100 ad ogni categoria
      }

      for (i<-0 until set1.size){ //converto il set in sequenza e con i numeri che ho nella seq prendo le domande
        val s=set1.toSeq
        val l=(lista(s(i))) //dalla lista prenderò solo le domande con gli id random che ho generato
        listaDom = l :: listaDom //aggiungo le domande pescate nella lista domande
      }
      j+=1
      set1.clear()//pulisco il set così metto altri 10 numeri
    }
    listaDom=listaDom.reverse //le domande vengono inserite in modo lifo ma noi le voglioamo in oridne di inserimento
    listaDom=listaDom.drop(1) //tolgo il primo elemento che è vuoto, lo aggiunge appena creo listadom

  }

  private def elaboradomande(): Unit = { //serve a leggere tutte le domande nel file
    var primaRiga=true
    for (line <- bufferedSource.getLines) {//leggo tutte le linee del file
      if (primaRiga) { //controllo se sono alla prima riga
        //faccio anche il replace delle " perchè danno problemi in fase di invio delle domande nella socket
        //quello che leggo lo mentto nelle colonne per questo faccio la mappa, per sicurezza faccio trim che rimuove
        //gli spazi bianchi
        val cols = line.replace("\"","").split(";").map(_.trim)
        val l = cols.length
        for (i <- 0 until  l ) {
          key += (cols(i)->"0")   //la prima riga contiene solo le key e 0 al posto di un valore vero
        }
        primaRiga=false
        lista=key::lista //le aggiungo alla lista, per ora contiene solo la prima riga che ha solo info e non domande vere e proprie
      }
      else {
        val cols = line.replace("\"","").split(";").map(_.trim) //come prima ma ora ci sono le domande
        val l = cols.length
        val s = key.keys.toSeq //prendo le key che mi servono per la mappa che sarà del tipo k->v

        for (i <- 0 until l ) { // in s ci sono le key fatte a sequenza per praticità le metto in s, in cols i valori
          dict+= (s(i) -> cols(i)) //metto nella mappa,come sopra ma ora ci sono valori veri e propri
        }
        lista=dict.clone()::lista// senza il clone copia sempre il primo mentre così sono sicuro copia quello corrente
      }
    }
    lista = lista.reverse//anche qua faccio il reverse per averle in ordine di inserimento
    lista = lista.drop(1)// levo il primo che è vuoto
    bufferedSource.close//chiudo il buffer
  }

}
