import BandMatrix
import CAHDalgorithm
import time
import numpy as np
import KLDivergence
import operator
import random
import getopt
import sys

if __name__ == "__main__":
    dim_finale = 100
    num_sensibile = 10
    grado_privacy = 6
    q_value_list = [np.random.uniform(0, 0.5) for index in range(10)]
    alpha = 3
    nameFile = "Dataset/BMS1.csv"
    listaItem = "Dataset/Items_BMS1.txt"

    r = 4  # numero di QID nella query
    max_attempts = 1

    # controllo gli eventuali argomenti di command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:i:n:m:p:q:r:x:", ["dataset=", "items=", "n=", "m=", "p=", "qvalues=", "r=", "maxattempts="])
    except getopt.GetoptError:
        print(
            'Main_Density-Qvalues_Analysis.py\n'+
            ' -d <path del dataset>\n'+
            ' -i <path del file con i codici prodotti>\n'+
            ' -n <dimensione matrice quadrata>\n'+
            ' -m <numero attributi sensibili>\n'+
            ' -p <grado di privacy>\n'+
            ' -q <valori di q, intervallati da virgola>\n'+
            ' -r <valore di r>\n'+
            ' -x <numero di ripetizioni>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                'Main_Density-Qvalues_Analysis.py\n' +
                ' -d <path del dataset>\n' +
                ' -i <path del file con i codici prodotti>\n' +
                ' -n <dimensione matrice quadrata>\n' +
                ' -m <numero attributi sensibili>\n' +
                ' -p <grado di privacy>\n' +
                ' -q <valori di q, intervallati da virgola>\n' +
                ' -r <valore di r>\n' +
                ' -x <numero di ripetizioni>')
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

    coeff = (1/max_attempts)*0.195
    for i in range(max_attempts):

        """
        # Codice per la generazione di dataset a densità definita
        file_dataset = open(nameFile, "w")
        text = ""

        # intervallo di densità variabile in funzione del valore di i
        max_d = (0.2 - (coeff * i))/(dim_finale/10)
        min_d = (max_attempts-i)/(12 * max_attempts * dim_finale / 10)

        #Attuale densità
        t_d = random.uniform(min_d , max_d)
        print("Density : "+str(t_d))

        #scrivo file del dataset
        for j in range(dim_finale):
            for k in range(dim_finale+num_sensibile):
                actual_dimension = random.uniform(0, 1)
                if actual_dimension < t_d:
                    text += "1"
                else:
                    text += "0"
                if k < dim_finale+num_sensibile-1:
                    text += ","
                else:
                    text += "\n"
            file_dataset.write(text)
        file_dataset.close()
        
        #scrivo file con codici prodotto
        file_list = open(listaItem, "w")
        for j in range(dim_finale + num_sensibile):
            file_list.write(str(j)+"\n")
        file_list.close()
        """

        print("Read Dataset")
        df = BandMatrix.BandMatrix(nameFile)
        print("Calcolo la band matrix")
        df.compute_band_matrix(
            dim_finale=dim_finale,
            nome_file_item=listaItem,
            num_sensibile=num_sensibile)
        KLs = list()
        for iii in range(len(q_value_list)):
            #valore di q in questo tentativo
            q_value = q_value_list[iii]
            start_time = time.time()
            cahd = CAHDalgorithm.CAHDalgorithm(
                df,
                grado_privacy=grado_privacy,
                alfa=alpha,
                q_value=q_value)
            cahd.compute_hist()
            hist_item = cahd.hist
            print("Eseguo Anonimizzazione")
            if cahd.CAHD_algorithm(analysis=True):
                end_time = time.time() - start_time
                print("Execution time for privacy %s is %s" % (grado_privacy, end_time))
                all_item = list(df.items_final.keys())
                columns_item_sensibili = df.lista_sensibili
                dataframe_bandizzato = df.dataframe_bandizzato
                QID = cahd.lista_gruppi[0].columns.tolist()
                QID_select = list()
                while len(QID_select) < r:
                    temp = random.choice(QID)
                    if temp not in QID_select:
                        QID_select.append(temp)
                all_value = KLDivergence.get_all_combination_of_n(r)
                item_sensibile = int(max(hist_item.keys(), key=(lambda k: hist_item[k])))
                print(hist_item)
                print(item_sensibile)
                KL_Divergence = 0
                for valori in all_value:
                    actsc = KLDivergence.compute_act_s_in_c(dataframe_bandizzato, QID_select, valori, item_sensibile)
                    estsc = KLDivergence.compute_est_s_in_c(dataframe_bandizzato, cahd.sd_gruppi, cahd.lista_gruppi,
                                                            QID_select, valori, item_sensibile)
                    if actsc > 0 and estsc > 0:
                        temp = actsc * np.log(actsc / estsc)
                    else:
                        temp = 0
                    KL_Divergence = KL_Divergence + temp
                KLs.append(KL_Divergence)
        min_index, min_value = min(enumerate(KLs), key=operator.itemgetter(1))
        file_d = open("DensityQ/KL-Divergence-Density.txt", "a")
        file_q = open("DensityQ/KL-Divergence-Q-Value.txt", "a")
        comp = 0.0

        square_column_index = [x for x in df.dataframe_bandizzato.columns if x not in df.lista_sensibili]
        sum_for_columns = df.dataframe_bandizzato[square_column_index].sum()
        sum_total = 0
        for sum_column in sum_for_columns:
            sum_total += sum_column
        density = sum_total / (dim_finale * dim_finale)

        for j in range(len(KLs)):
            comp = KLs[j]
            if comp == min_value and comp != 99999:
                file_d.write(str(density)+";")
                file_q.write(str(q_value_list[j])+";")
        if min_value != 99999:
            print("-------------------------------------------")
        file_d.close()
        file_q.close()