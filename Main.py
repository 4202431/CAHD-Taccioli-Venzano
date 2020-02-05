import time
import BandMatrix
import CAHDalgorithm
import OutputData
import getopt
import sys

"""
    Main principale per la 
    chiamata alle classi 
    BandMatrix & CAHDalgorithm
"""

if __name__ == "__main__":
    dim_finale = 250  # dimensione massima matrice
    num_sensibile = 13  # n° dati sensibili
    grado_privacy = 10  # grado di privacy richiesto
    alpha = 3

    # lettura da file del dataset
    nameFile = "Dataset/BMS1.csv"
    listaItem = "Dataset/Items_BMS1.txt"

    # controllo gli eventuali argomenti di command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:i:n:m:p:", ["dataset=", "items=", "n=", "m=", "p="])
    except getopt.GetoptError:
        print('Main.py \n'+
              ' -d <path del dataset>\n'+
              ' -i <path del file con i codici prodotti>\n'+
              ' -n <dimensione matrice quadrata>\n'+
              ' -m <numero attributi sensibili>\n'+
              ' -p <grado di privacy>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Main.py \n' +
                  ' -d <path del dataset>\n' +
                  ' -i <path del file con i codici prodotti>\n' +
                  ' -n <dimensione matrice quadrata>\n' +
                  ' -m <numero attributi sensibili>\n' +
                  ' -p <grado di privacy>')
            sys.exit()
        elif opt in ("-d", "--dataset"):
            nameFile = arg
        elif opt in ("-i", "--items"):
            listaItem = arg
        elif opt in ("-n", "--n"):
            dim_finale = int(arg)
        elif opt in ("-m", "--m"):
            num_sensibile = int(arg)
        elif opt in ("-p", "--p"):
            grado_privacy = int(arg)

    print("Read Dataset")

    # partenza cronometro per registrazione prestazioni
    start_time = time.time()
    print("Calcolo la band matrix" + "\n")
    df = BandMatrix.BandMatrix(nameFile)

    # calcolo matrice banda
    df.compute_band_matrix(
        dim_finale=dim_finale,
        nome_file_item=listaItem,
        num_sensibile=num_sensibile)

    # applicazione algoritmo CAHD
    cahd = CAHDalgorithm.CAHDalgorithm(
        df,
        grado_privacy=grado_privacy,
        alfa=alpha)
    print("Eseguo Anonimizzazione")
    if cahd.CAHD_algorithm():
        end_time = time.time() - start_time
        print("Il tempo di esecuzione per il grado di privacy %s è %s" % (cahd.grado_privacy, end_time))
        print("")

        pr = OutputData.Printer(cahd, df)
        pr.stampa_gruppi()
        print("Control data")
        pr.controllo_dati(control=True)
