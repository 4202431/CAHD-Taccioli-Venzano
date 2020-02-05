Taccioli Gabriele 4234616 - Venzano Emanuele 4202431

Data Protection and Privacy - Anonimizzazione di dati transazionali con algoritmo CAHD

Il nostro progetto è composto di 11 programmi eseguibili e 5 classi di supporto. Gli eseguibili possono essere divisi in 3 diverse categorie:
- Funzionamento base di CAHD
- Analisi delle prestazioni di CAHD 
- Funzionamento ed analisi di un possibile miglioramento dell'algoritmo CAHD
Per ogni eseguibile è possibile passare i parametri da console o usare quelli di default già inseriti nel codice. In code al README sono presenti in dettaglio i parametri da passare a ogni eseguibile, ma è comunque possibile passare al singolo eseguibile il parametro -h per poter visualizzare le stesse informazioni.


CLASSI DI SUPPORTO
- BandMatrix: predispone i dati iniziali leggendo da file il dataset e i relativi codici prodotto,  scegliendo randomicamente le righe e le colonne su cui fare l'analisi e (se non viene specificato withRCM=False) bandizzando la matrice.
-BandMatrix_QStudy: utilizzato dal solo Main_Qvalues_Analysis, è una modifica della classe precedente che permette di modificare la densità della matrice quadrata con una densità specificata.
- CAHDalgorithm: è il core dell'algoritmo di anonimizzazione, crea i gruppi e restituisce una struttura dati anonimizzata.
- KLDivergence: classe di supporto che permette di calcolare la KL-Divergence.
-OutputData: classe di supporto che contiene un metodo per stampare il dataset anonimizzato e un metodo per controllare la consistenza tra i dati nel dataset anonimizzato e in quello originale.

FUNZIONAMENTO BASE DI CAHD
L'algoritmo CAHD viene implementato nella sua forma standard in Main.py. Viene letto un file .csv contenente le transazioni, vengono estretti randomicamente un certo numero (passato da console o stabilito di default) di attributi sensibili e viene bandizzata la matrice relativa ai QID. Viene applicato l'algoritmo CAHD per creare i gruppi anonimizzati. La struttura dati contenente il dataframe anonimizzato è costruita da:
- un dizionario le cui chiavi sono gli indice dei gruppi e i valori gli indici delle transazioni del gruppo.
- una lista in cui a ogni indice (che individua un gruppo) è associato il sotto-dataframe dato dalle transazioni del gruppo e dai QID
- una lista in cui a ogni indice (che individua un gruppo) è associata una seria i cui indici sono gli indice degli attributi sensibili e i cui valori sono le corrispettive occorrenze nel gruppo.
Il dataframe anonimizzato viene poi passato ad OutputData che ne mostra a video la soluzione e controlla che le transazioni relativamente ai QID nel dataframe anonimizzato siano le stesse di quello originale, e che la somma degli attributi sensibli nel gruppo sia la stessa di quelli nel database originale relativamente alle transazioni del gruppo.
E' presente anche un secondo esguibile, Main_KL-Divergence, che in aggiunta al precedente calcola (su r QID) la divergenza del dataframe anonimizzato rispetto all'originale e ne mostra a video il risultato.

ANALISI DELLE PRESTAZIONI DI CAHD
Sono presenti 4 diversi file che analizzano le prestazioni dell'algoritmo da diversi punti di vista e ne scrivono i risultati su file. Un quinto script è poi dedicato a leggere i file e farne il plotting, in modo da poter disporre di un gran numero di dati e non perdere quelli relativi alle precedenti esecuzioni del programma. I nomi dei file di output sono composti dalle specifiche della singola esecuzione, in modo da venire comparati solo con configurazioni analoghe.
Nello specifico:
- Main_Privacy-KLD_Analysis: al variare del numero di attributi sensibili e del grado di privacy viene calcolata la divergenza, che viene poi visualizzata sull'asse y. Sull'asse x viene visualizzata la privacy, mentre il numero di attributi sensibili individua una diversa traccia nel grafico. Il file viene salvato nella cartella MainPlotData/0/ e viene individuato dal nome del dataset, la dimensione della matrice quadrata, il numero di QID su cui calcolare la KLD e il numero di ripetizioni della KLD per ottenere un risultato più attendibile.
- Main_Sensitive-KLD_Analysis: analogamente a prima, viene calolata la divergenza al variare del numero di attributi sensibili e del grado di privacy desiderato. A differenza della precedente analisi sull'asse x viene visualizzato il numero di attributi sensibili e il grado della privacy individua le diverse traccie nel grafico. I file vengono salvati analogamente al precedente, ma nella cartella MainPlotData/1/
- Main_R-KLD_Analysis: viene svolta un'analisi della  divergenza al variare del numero di QID su cui calcolarla (r, asse x) e del grado di privacy (p, identifica le diverse tracce). I file di output vengono salvati nella cartella MainPlotData/2/ e i loro nomi comprendono nome del dataset, dimensione della matrice dei QID, numero di attributi sensibili e numero di ripetizioni del calcolo di KLD
- Main_Privacy-Time_Analysis: viene svolta un'analisi sul tempo richiesto dall'algoritmo al variare del grado di privacy (asse x) e del'utilizzo o meno del algoritmo di banidizzazione della matrice dei QID. I file vengono salvati in MainPlotData/3/ e i loro nomi contengono nome del dataset, dimensionde della matrice quadrata e numero di attributi sensibili.
- Main_Plot_Analysis: specificando i nomi dei file presenti nelle diverse cartelle vengono tracciati i grafici delle varie analisi dell'algoritmo CAHD.

FUNZIONAMENTO ED ANALISI DI UN POSSIBILE MIGLIORAMENTO
Abbiamo ritenuto interessante provare a modificare il criterio di somiglianza delle transazioni nella creazioni dei gruppi all'interno dell'algoritmo CAHD, introducendo un coefficiente q da moltiplicare per il numero di attributi non presenti in nessuna delle due transazioni in esame. Abbiamo studiato come vari il valore di questo coefficiente in funzione della densità della matrice quadrata, cioè della probabilità di coppie "1-1" e "0-0" nel confronto tra due transazioni.
Abbiamo sviluppato 3 algoritmi di analisi, che salvano in cartelle diverse i risultati ottenuti. Per l'analisi dei primi due abbiamo utilizzato MatLab, cercando di calcolare la funzione tra input e output mediante un metodo di regressione non lineare, per l'ultima abbiamo sviluppato un ulteriore script in python che ne permetta un'analisi più qualitative facendo il plotting dei  dati.
Nello specifico:
- Main_Density-Qvalues_Analysis: mantenendo fissato il numero di attributi sensibili e il grado privacy, calcoliamo la divergenza utilizzando diversi valori di q su una stessa matrice bandizzata, andando a scrivere su file quale/i valore/i di q hanno minimizzato la divergenza dell'attuale configurazione. Per permettere la creazione di file aventi la densità desiderata è presente all'interno la possibilità di farlo a runtime. I file di output KL-Divergence-Density e KL-Divergence-Q-Value vengono salvati nella cartella DensityQ.
- Main_Qvalues-KLD_Analysis: mantenendo fissato il numero di attributi sensibili, il grado privacy e il dataset (preso nella sua interezza, in modo da ottenere in media sempre la stessa densità), andiamo a calcolare la KLD in funzinoe dei valori q scelti. I file di output q_values e divergences vengono salvati nella cartella Q-KLD.
- Main_Qvalues_Analysis: utilizzando una opportuna classe BandMatrix_QStudy, andiamo a fare l'analisi di un dataset andando a modificare la densità della sola parte di matrice contenente i QID. Vengono salvati nella cartella Q-Study quattro diversi file, contenenti informazioni relative ai valori di q e della densità, il tempo necessario all'esecuzione dell'istanza, il valore di KLD che ne deriva e il numero di gruppi ottenuti nel dataframe anonimizzato. I quattro file condividono una parte del nome (quella relativa al nome del dataset, alla dimensione della matrice quadrata, del grado privacy, del numero di attributi senisbli, al valore di r e al numero di volte in cui viene calcolata KLD) e terminano rispettivamente con input, time, divergence e exit.
- Main_Plot_Qvalues_Analysis: lo script viene utilizzato per analizzare i file sopra indicati, generando quattro diversi plot per quanto rigurada la divergenza (il primo con tutti i dati, il secondo eliminando gli outliers con un metodo basato sulla deviazione standard, il terzo e il quarto analizzando i soli valori minimi e massimi della divergenza), due diversi plot per il tempo necessario (uno con tutti i dati e uno eliminando gli outliers) e uno per il numero di gruppi generati dall'algoritmo CAHD.

PARAMETRI DA PASSARE AI SINGOLI ESEGUIIBLI
In alcuni dei parametri visualizzati in seguito sarà presente la dicitura "intervallati da virgola". Per questi, viene data la possibilità all'utilizzatore di usare un array di valori, che dovranno essere inseriti da linea di comando separati da virgole e senza spazi.

Main.py 
 -d <path del dataset>
 -i <path del file con i codici prodotti>
 -n <dimensione matrice quadrata>
 -m <numero attributi sensibili>
 -p <grado di privacy>

Main_Density-Qvalues_Analysis.py
 -d <path del dataset>
 -i <path del file con i codici prodotti>
 -n <dimensione matrice quadrata>
 -m <numero attributi sensibili>
 -p <grado di privacy>
 -q <valori di q, intervallati da virgola>
 -r <valore di r>
 -x <numero di ripetizioni>

Main_KL-Divergence.py
 -d <path del dataset>
 -i <path del file con i codici prodotti>
 -n <dimensione matrice quadrata>
 -m <numero attributi sensibili>
 -p <grado di privacy>

Main_Plot_Analysis.py
 -f <path della cartella>
 -i <nomi dei file di cui fare plotting, intervallati da virgola>
 -x <etichette assi x, intervallate da virgola>
 -y <etichette assi y, intervallate da virgola>
 -v <etichette altre variabili, intervallate da virgola>

Main_Plot_Qvalues_Analysis.py 
 -f <path della cartella>
 -i <nome file di input>
 -d <nome file con risultati di diverenza>
 -e <nome file con risultati sull'esito>
 -t <nome file con risultati sul tempo>

Main_Privacy-KLD_Analysis.py 
 -d <path dei dataset, intervallati da virgola>
 -i <path dei file con i codici prodotti, intervallati da virgola>
 -n <dimensione matrice quadrata>
 -m <numeri attributi sensibili, intervallati da virgola>
 -p <gradi di privacy, intervallati da virgola>
 -r <valore di r>
 -x <numero di ripetizioni>
 -k <numero di ripetizioni su cui mediare KLD>

Main_Privacy-Time_Analysis.py 
 -d <path dei dataset, intervallati da virgola>
 -i <path dei file con i codici prodotti, intervallati da virgola>
 -n <dimensione matrice quadrata>
 -m <numero attributi sensibili>
 -p <gradi di privacy, intervallati da virgola>
 -x <numero di ripetizioni>

Main_Qvalues-KLD_Analysis.py
 -d <path del dataset>
 -i <path del file con i codici prodotti>
 -n <dimensione matrice quadrata>
 -m <numero attributi sensibili>
 -p <grado di privacy>
 -q <valori di q, intervallati da virgola>
 -r <valore di r>
 -x <numero di ripetizioni>
 -k <numero di ripetizioni su cui mediare KLD>

Main_Qvalues_Analysis.py 
 -f <path del dataset>
 -i <path del file con i codici prodotti>
 -n <dimensione matrice quadrata>
 -m <numero attributi sensibili>
 -p <grado di privacy>
 -r <valore di r>
 -x <numero di ripetizioni>
 -k <numero di ripetizioni su cui mediare KLD>
 -d <valore minimo di densità>
 -D <valore massimo di densità>
 -q <valore minimo di q>
 -Q <valore massimo di q>
 -t <numero di valori di densità da provare>
 -T <numero di valori di q da provare>

Main_R-KLD_Analysis.py 
 -d <path dei dataset, intervallati da virgola>
 -i <path dei file con i codici prodotti, intervallati da virgola>
 -n <dimensione matrice quadrata>
 -m <numero attributi sensibili>
 -p <gradi di privacy, intervallati da virgola>
 -r <valori di r, intervallati da virgola>
 -x <numero di ripetizioni>
 -k <numero di ripetizioni su cui mediare KLD>

Main_Sensitive-KLD_Analysis.py 
 -d <path dei dataset, intervallati da virgola>
 -i <path dei file con i codici prodotti, intervallati da virgola>
 -n <dimensione matrice quadrata>
 -m <numeri attributi sensibili, intervallati da virgola>
 -p <gradi di privacy, intervallati da virgola>
 -r <valore di r>
 -x <numero di ripetizioni>
 -k <numero di ripetizioni su cui mediare KLD>
