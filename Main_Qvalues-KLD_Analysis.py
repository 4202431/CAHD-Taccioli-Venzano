import getopt
import sys

import BandMatrix
import CAHDalgorithm
import time
import numpy as np
import KLDivergence
import random

"""
    Main per l'esecuzione di matrice banda e 
    algoritmo CAHD con implementazione 
    valori di q e differenti tentativi per
    selezionare migliore a seconda di 
    valore di KL_Divergence
"""

if __name__ == "__main__":
    dim_finale = 50  # dimensione massima matrice
    num_sensibile = 6  # n° dati sensibili
    grado_privacy = 6  # grado di privacy richiesto
    q_value_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5]  # lista di valori di q da testare
    r = 8  # numero di QID nella query
    alpha = 3
    max_attempts = 30  # numero massimo tentativi
    kl_attempts = 4  # numero tentativi di calcolo di KL_Divergence

    # lettura da file del dataset
    nameFile = "Dataset/BMS1.csv"
    listaItem = "Dataset/Items_BMS1.txt"

    # controllo gli eventuali argomenti di command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:i:n:m:p:q:r:x:k:",
                                   ["dataset=", "items=", "n=", "m=", "p=", "qvalues=", "r=", "maxattempts=", "klattempts="])
    except getopt.GetoptError:
        print(
            'Main_Qvalues-KLD_Analysis.py\n' +
            ' -d <path del dataset>\n' +
            ' -i <path del file con i codici prodotti>\n' +
            ' -n <dimensione matrice quadrata>\n' +
            ' -m <numero attributi sensibili>\n' +
            ' -p <grado di privacy>\n' +
            ' -q <valori di q, intervallati da virgola>\n' +
            ' -r <valore di r>\n' +
            ' -x <numero di ripetizioni>\n'+
            ' -k <numero di ripetizioni su cui mediare KLD>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                'Main_Qvalues-KLD_Analysis.py\n' +
                ' -d <path del dataset>\n' +
                ' -i <path del file con i codici prodotti>\n' +
                ' -n <dimensione matrice quadrata>\n' +
                ' -m <numero attributi sensibili>\n' +
                ' -p <grado di privacy>\n' +
                ' -q <valori di q, intervallati da virgola>\n' +
                ' -r <valore di r>\n' +
                ' -x <numero di ripetizioni>\n' +
                ' -k <numero di ripetizioni su cui mediare KLD>')
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
        elif opt in ("-q", "--qvalues"):
            input_array = arg.split(",")
            q_value_list = [float(x) for x in input_array]
        elif opt in ("-r", "--r"):
            r = int(arg)
        elif opt in ("-x", "--maxattempts"):
            max_attempts = int(arg)
        elif opt in ("-k", "--klattempts"):
            kl_attempts = int(arg)

    df = BandMatrix.BandMatrix(nameFile)
    big_ben = time.time()

    # scansione fino al numero di tentativi richiesto
    for i in range(max_attempts):

        # calcolo matrice banda
        df.compute_band_matrix(
            dim_finale=dim_finale,
            nome_file_item=listaItem,
            num_sensibile=num_sensibile, plot=False)

        # calcolo items QID e somma valori nelle colonne QID
        KLs = [0, 0, 0, 0, 0, 0]
        dataframe_bandizzato = df.dataframe_bandizzato
        columns_item_sensibili = df.lista_sensibili
        QID = [x for x in dataframe_bandizzato.columns if x not in columns_item_sensibili]
        """
        QID_sensitive_rows = dataframe_bandizzato.iloc[list(set
                                                            (list(np.where(
                                                                dataframe_bandizzato
                                                                [df.lista_sensibili] == 1)[0])))].index
        QID_columns = [x for x in QID if x not in df.lista_sensibili]
        QID_sum = dataframe_bandizzato.iloc[QID_sensitive_rows][QID_columns].sum()
        QID = [x for x in QID_columns if QID_sum[x] > 0]
        """
        QID_select = list()
        while len(QID_select) < r:
            temp = random.choice(QID)
            if temp not in QID_select:
                QID_select.append(temp)

        # scansione tentativi di calcolo di KL_Divergence
        for kl_attempt in range(kl_attempts):
            QID_select = list()
            while len(QID_select) < r and len(QID_select) < len(QID):
                temp = random.choice(QID)
                if temp not in QID_select:
                    QID_select.append(temp)
            for iii in range(len(q_value_list)):
                q_value = q_value_list[iii]
                start_time = time.time()
                print("%.2f |Attempt : %s | KL_Attempt : %s | Indice di q : %s" % (
                    time.time() - big_ben, i, kl_attempt, iii))

                # applicazione algoritmo CAHD
                cahd = CAHDalgorithm.CAHDalgorithm(
                    df,
                    grado_privacy=grado_privacy,
                    alfa=alpha,
                    q_value=q_value)
                cahd.compute_hist()
                hist_item = cahd.hist
                if cahd.CAHD_algorithm(analysis=True, plot=False):
                    end_time = time.time() - start_time
                    print("Il tempo di esecuzione per il grado di privacy %s è %s" % (cahd.grado_privacy, end_time))
                    # calcolo di tutte le combinazioni per la cella C
                    all_value = KLDivergence.get_all_combination_of_n(r)
                    item_sensibile = int(max(hist_item.keys(), key=(lambda k: hist_item[k])))
                    KL_Divergence = 0
                    start_time2 = time.time()

                    # calcolo actsc e estsc richieste per KL_Divergence
                    for valori in all_value:
                        actsc = KLDivergence.compute_act_s_in_c(dataframe_bandizzato, QID_select, valori,
                                                                item_sensibile)
                        estsc = KLDivergence.compute_est_s_in_c(dataframe_bandizzato, cahd.sd_gruppi,
                                                                cahd.lista_gruppi,
                                                                QID_select, valori, item_sensibile)
                        if actsc > 0 and estsc > 0:
                            temp = actsc * np.log(actsc / estsc)
                        else:
                            temp = 0
                        KL_Divergence = KL_Divergence + temp
                    KLs[iii] += KL_Divergence
                    end_time2 = time.time() - start_time2
                # scrittura su file dei risultati ottenuti
                file_d = open("Q-KLD/q_values.txt", "a")
                file_q = open("Q-KLD/divergences.txt", "a")
                for j in range(len(KLs)):
                    comp = KLs[j] / kl_attempts
                    file_d.write(str(q_value_list[j]) + ";")
                    file_q.write(str(comp) + ";")
                file_d.close()
                file_q.close()
