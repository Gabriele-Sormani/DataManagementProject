DATA ACQUISITION SCRIPT:

AqiDataRetrival.py:
	Questo script permette di ottenere i dati relativi alla qualità dell'aria, tramite scraping dal sito https://aqicn.org/station/, lo scraping viene inizialmente effettuato usando la
	libreria Selenium, che si occupa nella fase iniziale di attendere il completo caricamento della pagina e estrarre il file HTML corrispondente, nel momento in cui gli elementi di 	nostro interesse per lo scraping sono completamente caricati. Il codice HTML viene successivamente analizzato tramite la libreria BeautifulSoup4 che si occupa di individuare i tag 	HTML che definiscono i contenuti da noi desiderati cioè i valori dell'indice di qualità dell'aria e i vari inquinanti. Il procedimento di scraping è contenuto all'interno 	dell'apposito metodo stationScraper che prende come parametro l'id della stazione di misurazione della qualità dell'aria; quest'ultimo usato per costruire l'URL della pagina web, 	poichè ogni stazione di rilevazione mostra le informazioni in una pagina web dedicata, di conseguenza per ognuno dei 17 sensori viene effettuato lo scraping in maniera automatica 	ad intervalli orari, i risultati dello scraping vengono salvati all'interno di un unico file json.

TrafficDataRetrival.py:
	Questo script permette di ottenere i dati relativi al traffico tramite l'utilizzo delle API fornite da HERE https://www.here.com/docs/bundle/traffic-api-v7-api-	reference/page/index.html#tag/Real-Time-Traffic/operation/getFlow. Inizialmente viene definita una bounding box che delinea l'area di interesse tramite coordinate geografiche, 	dopodichè viene costruito l'URL della chiamata alle API tramite api_key facendo riferimento all'endpoint /flow tramite metodo GET, passando come parametro della query la bound box 	definita precedentemente. Successivamente viene effettuata la chiamata all'endpoint API e in caso di risposta positiva dal server il contenuto della risposta viene salvato 	all'interno di un apposito file json, vista la pesantezza dei dati scaricati da questa API è stato messo un vincolo sulla dimensione dei file, quindi nel momento in cui questo 	supera 1GB di dimensione il file nel quale vengono salvate le risposte cambia, per questo motivo questo script produce più file come risultato. Questo script funziona in maniera
        automatica effettuando tutto il procedimento ad intervalli orari.

AqiSensorsAddress.py:
	Questo script permette di ottenere gli indirizzi relativi al posizionamento delle stazioni di qualità dell'aria tramite scraping dal sito https://aqicn.org/station/, lo scraping 	viene inizialmente effettuato usando la libreria Selenium, che si occupa nella fase iniziale di attendere il completo caricamento della pagina e estrarre il file HTML 	corrispondente nel momento in cui gli elementi di interesse per lo scraping sono completamente caricati. Il codice HTML viene successivamente analizzato tramite la libreria 	BeautifulSoup4 che si occupa di individuare l'intestazione della pagina ed estrarne il valore relativo all'idirizzo. Infine viene effettuato lo scraping su tutte le pagine web di
        tutti i sensori e i risultati vengono salvati su un file json.

AqiSensorsGeocoding.py:
	Questo script permette di ottenere le coordinate geografiche che descrivono il posizionamento delle stazioni di misurazione della qualità dell'aria distribuite sul territorio. Per 	effettuare questa operazione si è utilizzato il servizio di geocoding fornito dalle API di geoApify https://www.geoapify.com/geocoding-api?gclid=CjwKCAiA8YyuBhBSEiwA5R3-	E2pkpbBXUv9bCCJF4cODwryMQPT04ELPU9__iiuET4SN3cUNnru6CBoCCuUQAvD_BwE. Inizialmente vengono letti gli indirizzi dei vari sensori dall'apposito file, dopopdichè per ogni indirizzo 	contenuto nel file viene effettuata una chiamata all'endpoint /geocode tramite metodo GET, il quale restituisce la posizione dell'indirizzo passato trmite i parametri dell'URL. Le 	coppie latitudine e longitudine vengono poi salvate in un apposito file json

AqiAPI.py:
	Questo script permette di ottenere i dati relativi alla qualità dell'aria forniti da OpenMeteo https://open-meteo.com/en/docs/air-quality-api, i dati vengono ricavati tramite 	l'utilizzo delle API inizialmente viene definito il periodo di interesse come intervallo tra due date, dopodichè vengono estratte le posizioni dei sensori contenute nell'apposito 	file e per ognuna di queste viene effettuata una chiamata all'endpoint /air-quality tramite metodo GET, i parametri dell'URL sono costituiti da data di inizio, data di fine, il 	punto geografico e le misurazioni selezionate, effettuando la richiesta in caso di risposta positiva i dati vengono salvati in un apposito file json

MeteoDataRetrival.py:
	Questo script permette di ottenre i dati metereologici tramite il servizio di API fornito da Meteostat https://dev.meteostat.net/. Inizialmente viene definito il periodo di 	interesse specificando data di inizo e data di fine; per effettuare le chiamate alle API è stata utilizzata la libreria messa a disposizione da meteostat, che tramite l'utilizzo 	della funzione Hourly permette di ricavare i dati meteo orari all'interno del periodo di interesse. Un ulteriore parametro necessario per l'utilizzo della funzione Hourly è il 	punto geografico, questo script ricava i dati meteo per ognuna delle posizioni geografiche contenute nell'apposito file. I dati metereologici vengono salvati in file json separati 	dove ognuno di questi fa riferimento a una stazione di rilevazione della qualità dell'aria e contiene i dati nell'intervallo temporale specificato.



DATA STORAGE, DATA QUALITY, DATA INTEGRATION, DATA CLEANING, QUERIES E ANALISI ESPLORATIVA:

MongoRawData.ipynb
	Questo jupiter notebook si occupa della prima fase di data storage in cui i dati grezzi vengono salvati in collezioni separate su MongoDB. Per fare ciò viene utilizzata la libreria 	pymongo, la prima fase consiste nell'effettuare la connessione al database mongoDB tramite la funzione MongoClient che effettua la connessione al database, successivamente viene 	selezionato il database nel quale salvare i dati. E' stato definito un blocco di codice per ogni collection di documenti in cui salvare i dati grezzi tramite le funzioni insertMany 	e insertOne. All'interno del salvataggio su database relativo ai dati di traffico è stato necessario svolgere un salvataggio più elaborato a causa di un errore di encoding e a 	causa delle dimensioni dei singoli oggetti json i quali superano la dimensione massima consentita dei singoli BSON, di conseguenza prima del salvataggio le infromazioni relative al 	traffico salvate in un unica lista vengono estratte e poste nel database separatamente, inoltre tramite un controllo sulla lunghezza delle stringhe è stato parzialmente corretto 	l'errore di encoding.

DataQualityCleaningAndIntegration.ipynb
	Questo jupiter notebook si occupa delle fasi di data quality, data integration, data cleaning e del salvataggio dei dati puliti e integrati su database. 
	1) La prima operazione svolta sono le misure di data quality, vengono calcolate le metriche di data quality relative alla table completeness e attribute completeness per ogni 	collezione di dati grezzi, vengono calcolate delle metriche di data quality relative all'accuratezza dei dati metereologici, vengono calcolate le metriche di data quality relative 	alla consistenza di vari dati presenti nelel varie collections di dati grezzi.
	2) Come fase successiva vengono effettuate diverse operazioni di data cleaning e data integrazion, queste basate sia sulle metriche calcolate precedentemente sia su altre mancanze 	dei dati e altri problemi evidenti all'interno dei dati aggregati:
		- viene rimosso il parametro nullo pm1 dai dati relativi all'inquinamento
		- vengono integrate le informazioni geografiche delle stazioni di rilevazione all'interno dei dati metereologici
		- vengono rimossi i dati metereologici ottenuti dallo scraping a causa di problemi sia per quanto riguarda l'accuracy sia per la completeness
		- vengono rimossi gli attributi sempre nulli dai dati metereologici ricavati da meteostat
		- vengono convertite le velocità nei dati di traffico da m/s a km/h
		- viene ricavato il punto di inizio e di fine del tratto stradale
		- vengono rimossi gli attributi sempre nulli dai dati di traffico
		- vengono rimossi i record che presentano mancanze nei dati
		- viene completamente corretto l'errore di encoding all'interno degli indirizzi nei dati di traffico
		- viene associata ai dati di traffico la stazione di rilevazione della qualità dell'aria più vicina
		- vengono integrati tra di loro i dati cercando corrispondenze tra le infromazioni temporali e il codice della stazione meteo creando un unico dataset definitivo
		- vengono calcolati ulteriori dati: il giorno della settimana e la differenza tra velocità di percorrenza e velocità ideale
		- vengono convertite in formato numerico le misure relative agli inquinanti
	3) In seguito vengono ricalcolate le misure di data quality sui dati puliti e integrati 
	4) Infine viene salvato il dataset finale su mongoDB



Exploratory analysis.ipynb
	Questo jupiter notebook si occupa dell'analisi esplorativa dei dati, i quali vengono ricavati mediante queries al databse MongoDB, vengono effettuate delle query che leggono dati 	dal database in relazione al tipo di analisi da effettuare. vengono fatte diverse analisi che permettono di rispondere alle domande di ricerca tramite il calcolo di statistiche 	descrittive, visualizzazione dei dati e raggruppamento dei dati, è possibile dividere le analisi in 3 aree: relazione tra dati metereologici e dati sul traffico e inquinamento, 	relazione tra traffico e inquinamento e infine analisi dei dati in relazione al tempo e allo spazio. 

