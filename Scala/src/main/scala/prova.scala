import java.io.PrintStream
import java.net.{InetAddress, Socket}

import generatoreDomandeTest.lettoreDomande

import scala.collection.mutable._
import scala.io.BufferedSource
import scala.util.Random._
import scala.io.StdIn._


//prova git
object Hello extends App {
  var path="src/main/scala/questionario.csv"
  var obj= new lettoreDomande(path=path,2)// il numero è per devidere quante domande per ogni categoria
  var lista=obj.listaDom
  //println(lista)
  var IdDomande=List[Int]()//metto gli id delle domande
  var PunteggioDomande=List[Double]() //metto le risposte
  var RisposteSelezionate=List[String]()//metto le risposte scelte
  var DomandeUscite=List[String]()//metto le domande
  var CategorieDomande=List[String]()
  /*println(lista)
  println(lista.length)*/
  val nome=readLine("inserisci nome: ")
  val cognome=readLine("inserisci cognome: ")
  println(nome,cognome)

  for(i<-lista.indices){//serve per scorrere tra le domande
    var risp = LinkedHashMap[String,String]() //metto le risposte quando poi faccio lo shuffle, ci saranno 4 risposte
    var risposta = -1 //metto il numero della risposta
    val h=lista(i).toList.head._2.toInt //serve pre prendere id della domanda
    IdDomande=h::IdDomande//tutto sto casino per prendere id che per qualche assurdo motivo non funziona con la mappa
    //prendo solo le risposte e le mischio perchè se no la prima è sempre quella giusta
    var keys= lista(i).keys.drop(3)// mi servono solo le risposte quindi elimino i primi 3 che sono id,cat,dom
    keys=shuffle(keys) //faccio uno shuffle per mischiare le risposte altrimenti la prima è sempre quella giusta
    for(k <- keys){
      risp+=k->lista(i)(k)//numeroRisposta->risposta
    }
    DomandeUscite=lista(i)("Domanda")::DomandeUscite //metto le domande che escono
    CategorieDomande=lista(i)("Categoria")::CategorieDomande
    println("-"*150)
    println("CATEGORIA:\t"+lista(i)("Categoria"))
    println("DOMANDA:\t"+lista(i)("Domanda"))
    for (j<-0 until keys.size) {
      println(j+1+")\t" + (risp(keys.toList(j)))) //serve per stampare le risposte
    }
    println("5)\tNON LA SO")

    while (risposta <0 | risposta >5) { //controllo che sia una delle risposte selezionate
      println("Inserisci una risposta tra 0 e 5: \t")
      try {
        risposta = readInt()

        if (risposta<5){ // ho due casi quando è giusta e quando è sbagliata
          RisposteSelezionate=(lista(i)(keys.toList(risposta-1)))::RisposteSelezionate //metto la risposta che ho scelto nella lista
          if(keys.toList(risposta-1) equals("Risposta_Corretta")){ //risposta-1 perchè gli indici partono da 0
            //println("ripsosta corretta")
            PunteggioDomande=1::PunteggioDomande
          } else {
            PunteggioDomande= -0.25::PunteggioDomande
          }
        }else if(risposta==5){
          PunteggioDomande= 0::PunteggioDomande
        }
      }catch {
        case e: Exception =>println("INSERIRE UN NUMERO DA 0 A 5, LETTERE NON CONSENTITE")
      }

    }
  }

  println("-"*150)
  DomandeUscite=DomandeUscite.reverse
  RisposteSelezionate=RisposteSelezionate.reverse
  IdDomande=IdDomande.reverse
  PunteggioDomande=PunteggioDomande.reverse
  CategorieDomande=CategorieDomande.reverse.distinct //serve per rimuovere i doppioni
  //print(PunteggioDomande)
  println("ID DOMANDE USCITE:\t"+IdDomande)
  println("DOMANDE USCITE:\t"+DomandeUscite)
  println("RISPOSTE SELEZIONATE:\t"+RisposteSelezionate)
  println("PUNTEGGIO RISPOSTE:\t"+PunteggioDomande)
  println("PUNTEGGIO TOTALE:\t"+PunteggioDomande.sum)
  println("CATEGORIE DOMANDE:\t"+CategorieDomande)

  val msg=  "{"+
    "\"Nome\": \""+ nome + "\", "+
    "\"Cognome\": \""+ cognome + "\", "+
    "\"IdDomande\": " + IdDomande.toArray.mkString("[", ", ", "]") + ", "+
    "\"CategorieDomande\": "+ CategorieDomande.toArray.mkString("[\"", "\", \"", "\"]") + ", "+
    "\"DomandeUscite\": "+ DomandeUscite.toArray.mkString("[\"", "\", \"", "\"]") + ", "+
    "\"RisposteSelezionate\": "+ RisposteSelezionate.toArray.mkString("[\"", "\", \"", "\"]") + ", "+
    "\"PunteggioDomande\": "+ PunteggioDomande.toArray.mkString("[", ", ", "]") +
  "}"
  println(msg)

  val s = new Socket(InetAddress.getByName("localhost"), 9999)

  val in = new BufferedSource(s.getInputStream).getLines()
  val out = new PrintStream(s.getOutputStream)
  /*out.println("Nome",nome,
    "Cognome",cognome,
    "IdDomande",IdDomande,
    "DomandeUscite",DomandeUscite,
    "RisposteSelezionate",RisposteSelezionate,
    "PunteggioDomande",RisposteSelezionate)*/

  out.println(msg)
  out.flush()
  //println("Received: " + in.next())

  s.close()


}

