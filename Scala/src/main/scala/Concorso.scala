import java.io.PrintStream
import java.net.{InetAddress, Socket}

import generatoreDomandeTest.lettoreDomande

import scala.collection.mutable._
import scala.io.BufferedSource
import scala.util.Random._
import scala.io.StdIn._
import util.Random


object Concorso{
  def main(args: Array[String]) = {
    val path = "src/main/scala/questionario.csv" //contiene le domande e le risposte
    //i test che voglio eseguire
    var numTest = 0
    var testEseguiti = 0
    val numDom = 10

    print("Eseguire simulazione true\\false?")
    val simulazione = readBoolean()
    if (simulazione) {
      println("HAI SCELTO SIMULAZIONE")
      while(numTest==0){
        print("Quanti test vuoi eseguire? Non puoi inserire 0:  ")
        try {
        numTest = readInt()
        }catch {
          case e: Exception => println("INSERIRE UN NUMERO VALIDO, NON SONO AMMESSI CARATTERI")
        }
      }
      println("Numero test che vuoi eseguire: "+ numTest)
    }else{
      println("NON E' UNA SIMULAZIONE")
      numTest=1
    }

    while (testEseguiti < numTest) {
      esecuzioneTest(numDom)
      testEseguiti = testEseguiti + 1
    }

    //mi genera il nome e il cognome
    def generaNomeCognome(): (String, String, String) = {
      val nomiPropri = Array("Agostino", "Alberto", "Alessandro", "Alessio", "Alfio", "Alfonso", "Amedeo", "Angelo", "Antonio", "Aurelio", "Corrado", "Cosimo")
      val cognomiPropri = Array("Rossi", "Ferrari", "Russo", "Bianchi", "Romano", "Gallo", "Costa", "Fontana", "Gialli", "Verdi")
      var codice = 0
      var nome = ""
      var cognome = ""
      if (!simulazione) {
        while (codice==0) {
          try {
            print("inserisci codice:")
            codice = readInt()
          }
          catch {
            case e: Exception => println("INSERIRE UN CODICE VALIDO, NON SONO AMMESSI CARATTERI")
          }
        }
        while (nome.length<=1 || cognome.length<=1){
          println("Sia nome che cognome devono avere più di un carattere")
          nome = readLine("inserisci nome: ")
          cognome = readLine("inserisci cognome: ")
        }
      } else {
        codice = Random.nextInt(100000)
        nome = nomiPropri(Random.nextInt(nomiPropri.length))
        cognome = cognomiPropri(Random.nextInt(cognomiPropri.length))
      }
      (nome, cognome, codice.toString)
    }


    def esecuzioneTest(numDom: Int): Unit = {
      //creo il lettore domande che mi ritorna una lista con delle domande random a cui devo rispodenre
      val obj = new lettoreDomande(path = path, numDom) // il numero è per devidere quante domande per ogni categoria
      val lista = obj.listaDom

      var IdDomande = List[Int]() //metto gli id delle domande
      var PunteggioDomande = List[Double]() //metto le risposte
      var RisposteSelezionate = List[String]() //metto le risposte scelte
      var DomandeUscite = List[String]() //metto le domande
      var CategorieDomande = List[String]() //lo uso per le categorie

      //scelgo nome e cognome random per semplicita di simulazione di un test
      val (nome, cognome, codice) = generaNomeCognome() //  readLine("inserisci nome: ")
      println("Ecco i tuoi dati: "+ nome+" "+cognome+" "+codice)
      for(elemento<-lista){ //serve per scorrere tra le domande
        //in pratica dalla elemento ottengo un ogetto che ha id,cat,dom, e 4 risposte
        //in pratica risp contiene le 4 possibili risposte, 1 ovviamente è quella giusta, è di tipo key value
        var risp = LinkedHashMap[String, String]() //metto le risposte quando poi faccio lo shuffle, ci saranno 4 risposte
        var risposta = -1 //metto il numero della risposta
        val h = elemento.toList.head._2.toInt //serve pre prendere id della domanda
        IdDomande = h :: IdDomande //per prendere id
        //prendo solo le risposte e le mischio perchè se no la prima è sempre quella giusta
        var keys = elemento.keys.drop(3) // mi servono solo le risposte quindi elimino i primi 3 che sono id,cat,dom
        keys = shuffle(keys) //faccio uno shuffle per mischiare le risposte altrimenti la prima è sempre quella giusta

        for (k <- keys) { //scorro le varie key che sono quelle delle risposte
          risp += k -> elemento(k) //numeroRisposta->risposta
        }
        DomandeUscite = elemento("Domanda") :: DomandeUscite //metto le domande che escono
        CategorieDomande = elemento("Categoria") :: CategorieDomande
        println("-" * 150)
        println("CATEGORIA:\t" + elemento("Categoria"))
        println("DOMANDA:\t" + elemento("Domanda"))

        //facendo così le risposte saranno stampate random perchè ho fatto lo shuffle delle key
        for (j <- 0 until keys.size) {
          println(j + 1 + ")\t" + (risp(keys.toList(j)))) //serve per stampare le risposte
        }
        println("5)\tNON LA SO")

        while (risposta < 1 | risposta > 5) { //controllo che sia una delle risposte selezionate
          try {
            println("Inserisci una risposta tra 1 e 5: \t")
            //metto random una risposta
            risposta = if (simulazione) Random.nextInt(5) + 1 else readInt() //così ho dei random tra 1 e 5  //1 //readInt()
            //risposta = readInt()//Random.nextInt(6)//1 //readInt()
            //println(risposta)
            if (risposta < 5) { // ho due casi quando è giusta e quando è sbagliata
              val scelta = keys.toList(risposta - 1)
              RisposteSelezionate = elemento(scelta) :: RisposteSelezionate //metto la risposta che ho scelto nella lista
              if (scelta equals ("Risposta_Corretta")) { //risposta-1 perchè gli indici partono da 0
                //entro qua se ho dato la risposta *****CORRETTA*****
                PunteggioDomande = 1 :: PunteggioDomande
              } else { //qua ho la risposta *****SBAGLAITA*****
                //PunteggioDomande = -0.25 :: PunteggioDomande
                val punti=if (simulazione) 0  else -0.25
                //println(punti)
                PunteggioDomande = punti :: PunteggioDomande
              }
            } else if (risposta == 5) { //qua mi sono *****ASTENUTO*****
              //PunteggioDomande = 0 :: PunteggioDomande
              val punti=if (simulazione) 0.25  else 0
              //println(punti)
              PunteggioDomande = punti :: PunteggioDomande
              RisposteSelezionate = "NON LA SO" :: RisposteSelezionate
            }
          } catch {
            case e: Exception => println("INSERIRE UN NUMERO DA 1 A 5, LETTERE NON CONSENTITE")
          } //TRY
        } //WHILE
      }
      println("-" * 150)
      DomandeUscite = DomandeUscite.reverse
      RisposteSelezionate = RisposteSelezionate.reverse
      IdDomande = IdDomande.reverse
      PunteggioDomande = PunteggioDomande.reverse
      CategorieDomande = CategorieDomande.reverse.distinct //serve per rimuovere i doppioni
      //print(PunteggioDomande)
      println("ID DOMANDE USCITE:\t" + IdDomande)
      println("DOMANDE USCITE:\t" + DomandeUscite)
      println("RISPOSTE SELEZIONATE:\t" + RisposteSelezionate)
      println("PUNTEGGIO RISPOSTE:\t" + PunteggioDomande)
      println("PUNTEGGIO TOTALE:\t" + PunteggioDomande.sum)
      println("CATEGORIE DOMANDE:\t" + CategorieDomande)
      generaDati(nome, cognome, codice, IdDomande, PunteggioDomande, RisposteSelezionate, DomandeUscite, CategorieDomande)

    }

    def generaDati(nome: String, cognome: String, codice: String,
                   IdDomande: List[Int],
                   PunteggioDomande: List[Double],
                   RisposteSelezionate: List[String],
                   DomandeUscite: List[String],
                   CategorieDomande: List[String]): Unit = {

      val msg = "{" +
        "\"Nome\": \"" + nome + "\", " +
        "\"Cognome\": \"" + cognome + "\", " +
        "\"Codice\": \"" + codice + "\", " +
        "\"IdDomande\": " + IdDomande.toArray.mkString("[", ", ", "]") + ", " +
        "\"CategorieDomande\": " + CategorieDomande.toArray.mkString("[\"", "\", \"", "\"]") + ", " +
        "\"DomandeUscite\": " + DomandeUscite.toArray.mkString("[\"", "\", \"", "\"]") + ", " +
        "\"RisposteSelezionate\": " + RisposteSelezionate.toArray.mkString("[\"", "\", \"", "\"]") + ", " +
        "\"PunteggioDomande\": " + PunteggioDomande.toArray.mkString("[", ", ", "]") +
        "}"
      println(msg)
      inviaDati(msg)
    }

    def inviaDati(msg: String): Unit = {
      var connesso=false
      while(!connesso) {//provo fino a quando non mi connetto
        try {
          val s = new Socket(InetAddress.getByName("localhost"), 9999)
          val out = new PrintStream(s.getOutputStream)
          val in = new BufferedSource(s.getInputStream).getLines()
          out.println(msg)
          out.flush()
          println(in.next())
          s.close()
          println(s)
          connesso=true
        }
        catch {
          case e: Exception => println("NON E' POSSIBILE CONNETTERSI CON LA SOCKET");connesso=false
        }
      }
      //Thread.sleep(10000)
    }
  }
}

