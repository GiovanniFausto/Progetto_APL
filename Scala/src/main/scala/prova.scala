import java.io.{BufferedReader, InputStreamReader, PrintStream}
import java.net.{InetAddress, Socket}

import generatoreDomandeTest.lettoreDomande

import scala.collection.mutable._
import scala.io.BufferedSource
import scala.util.Random._
/*TODO da mandare nome cognome IdDomande PunteggiDomande RIposteSelezionate DomandeUscite*/


object Hello extends App {
  var path="src/main/scala/questionario.csv"
  var obj= new lettoreDomande(path=path,1)// il numero è per devidere quante domande per ogni categoria
  var lista=obj.listaDom
  //println(lista)
  var IdDomande=List[Int]()//metto gli id delle domande
  var PunteggioDomande=List[Double]() //metto le risposte
  var RisposteSelezionate=List[String]()//metto le risposte scelte
  var DomandeUscite=List[String]()//metto le domande
  /*println(lista)
  println(lista.length)*/
  val nome=scala.io.StdIn.readLine("inserisci nome: ")
  val cognome=scala.io.StdIn.readLine("inserisci cognome: ")
  println(nome,cognome)

  for(i<-lista.indices){
    var risp = LinkedHashMap[String,String]()
    var risposta = -1
    val h=lista(i).toList(0)._2.toInt
    IdDomande=h::IdDomande//tutto sto casino per prendere id che per qualche assurdo motivo non funziona con la mappa
    //prendo solo le risposte e le mischio perchè se no la prima è sempre quella giusta
    var keys= lista(i).keys.drop(3)// mi servono solo le risposte
    keys=shuffle(keys)
    for(k <- keys){
      risp+=k->lista(i)(k)//numeroRisposta->risposta
    }
    DomandeUscite=lista(i)("Domanda")::DomandeUscite
    println("-"*150)
    println("CATEGORIA:\t"+lista(i)("Categoria"))
    println("DOMANDA:\t"+lista(i)("Domanda"))
    for (j<-0 until keys.size) {
      println(j+1+")\t" + (risp(keys.toList(j)))) //serve per stampare le risposte
    }
    println("5)\tNON LA SO")

    while (risposta <0 | risposta >5) { //controllo che sia una delle risposte selezionate
      println("Inserisci una risposta tra 0 e 5: \t")
      risposta = scala.io.StdIn.readInt()
      if (risposta<5){ // ho due casi quando è giusta e quando è sbagliata
        RisposteSelezionate=(lista(i)(keys.toList(risposta-1)))::RisposteSelezionate //metto la risposta che ho scelto nella lista
        if(keys.toList(risposta-1) equals("Risposta_Corretta")){
          println("ripsosta corretta")
          PunteggioDomande=1::PunteggioDomande
        } else {
          PunteggioDomande= -0.25::PunteggioDomande
        }
      }else if(risposta==5){
        PunteggioDomande= 0::PunteggioDomande
      }
    }
  }

  println("-"*150)
  DomandeUscite=DomandeUscite.reverse
  RisposteSelezionate=RisposteSelezionate.reverse
  IdDomande=IdDomande.reverse
  PunteggioDomande=PunteggioDomande.reverse
  //print(PunteggioDomande)
  println("ID DOMANDE USCITE:\t"+IdDomande)
  println("DOMANDE USCITE:\t"+DomandeUscite)
  println("RISPOSTE SELEZIONATE:\t"+RisposteSelezionate)
  println("PUNTEGGIO RISPOSTE:\t"+PunteggioDomande)

  //val socket = new Socket("localhost",9999)
  /*val s = new Socket(InetAddress.getByName("localhost"), 9999)
  val in = new BufferedSource(s.getInputStream).getLines()
  val out = new PrintStream(s.getOutputStream)
  out.println(nome,cognome,IdDomande,DomandeUscite,RisposteSelezionate,PunteggioDomande)
  out.flush()
  print("Received: " + in.next())
  s.close()*/


}

