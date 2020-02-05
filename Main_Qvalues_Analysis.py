import getopt
import sys

import BandMatrix_QStudy
import CAHDalgorithm
import time
import numpy as np
import KLDivergence
import random

if __name__ == "__main__":
    alpha = 3
    nameFile = "Dataset/BMS1.csv"
    listaItem = "Dataset/Items_BMS1.txt"
    dim_finale = 471
    num_sensibile = 10
    grado_privacy = 8
    kl_attempts = 7
    r = 7
    max_attempts = 20
    density_attempts = 10
    min_d = 0
    max_d = 0.6
    q_value_attempts = 4
    min_q = 0
    max_q = 0.6

    # controllo gli eventuali argomenti di command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:i:n:m:p:r:x:k:d:D:q:Q:t:T:",
                                   ["dataset=", "items=", "n=", "m=", "p=", "r=", "maxattempts=", "klattempts=", "mind=", "maxd=", "minq=", "maxq=", "dtime=", "qtime="])
    except getopt.GetoptError:
        print('Main_Qvalues_Analysis.py \n' +
              ' -f <path del dataset>\n' +
              ' -i <path del file con i codici prodotti>\n' +
              ' -n <dimensione matrice quadrata>\n' +
              ' -m <numero attributi sensibili>\n' +
              ' -p <grado di privacy>\n' +
              ' -r <valore di r>\n' +
              ' -x <numero di ripetizioni>\n' +
              ' -k <numero di ripetizioni su cui mediare KLD>\n'+
              ' -d <valore minimo di densità>\n' +
              ' -D <valore massimo di densità>\n' +
              ' -q <valore minimo di q>\n' +
              ' -Q <valore massimo di q>\n' +
              ' -t <numero di valori di densità da provare>\n' +
              ' -T <numero di valori di q da provare>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Main_Qvalues_Analysis.py \n' +
                  ' -f <path del dataset>\n' +
                  ' -i <path del file con i codici prodotti>\n' +
                  ' -n <dimensione matrice quadrata>\n' +
                  ' -m <numero attributi sensibili>\n' +
                  ' -p <grado di privacy>\n' +
                  ' -r <valore di r>\n' +
                  ' -x <numero di ripetizioni>\n' +
                  ' -k <numero di ripetizioni su cui mediare KLD>\n' +
                  ' -d <valore minimo di densità>\n' +
                  ' -D <valore massimo di densità>\n' +
                  ' -q <valore minimo di q>\n' +
                  ' -Q <valore massimo di q>\n' +
                  ' -t <numero di valori di densità da provare>\n' +
                  ' -T <numero di valori di q da provare>')
            sys.exit()
        elif opt in ("-f", "--dataset"):
            nameFile = arg
        elif opt in ("-i", "--items"):
            listaItem = arg
        elif opt in ("-n", "--n"):
            dim_finale = int(arg)
        elif opt in ("-m", "--m"):
            num_sensibile = int(arg)
        elif opt in ("-p", "--p"):
            grado_privacy = int(arg)
        elif opt in ("-r", "--r"):
            r = int(arg)
        elif opt in ("-x", "--maxattempts"):
            max_attempts = int(arg)
        elif opt in ("-k", "--klattempts"):
            kl_attempts = int(arg)
        elif opt in ("-d", "--mind"):
            min_d = int(arg)
        elif opt in ("-D", "--maxd"):
            max_d = int(arg)
        elif opt in ("-q", "--mind"):
            min_q = int(arg)
        elif opt in ("-Q", "--maxd"):
            max_q = int(arg)
        elif opt in ("-t", "--dtime"):
            density_attempts = int(arg)
        elif opt in ("-T", "--qtime"):
            q_value_attempts = int(arg)

    print("Read Dataset")
    df = BandMatrix_QStudy.BandMatrixQ2(nameFile)
    print("")

    big_ben = time.time()
    random_column = np.random.permutation(df.dataframe.shape[1])
    for i in range(max_attempts):
        random_column = np.random.permutation(df.dataframe.shape[1])[:dim_finale + num_sensibile]
        random_row = np.random.permutation(df.dataframe.shape[0])[:dim_finale]
        lista_sensibili = list()
        SD_zeros = list()
        while len(lista_sensibili) < num_sensibile:
            temp = np.random.choice(random_column)
            if temp not in lista_sensibili and temp not in SD_zeros:
                if df.dataframe[temp].sum() > 0:
                    lista_sensibili.append(temp)
                else:
                    SD_zeros.append(temp)
        columns = [x for x in random_column if x not in lista_sensibili]
        for g in range(density_attempts):
#            dens1 = np.random.uniform((g/density_attempts)*0.3, ((g/density_attempts)+0.001)*0.65)
            dens1 = np.random.uniform(min_d, max_d)
            df.compute_band_matrix(
                dim_finale=dim_finale,
                lista_sensibili_r=random_row,
                lista_sensibili_column=lista_sensibili,
                QID_columns=columns,
                density=dens1)
            dim_finale = df.size_after_RCM

            all_item = list(df.items_final.keys())
            columns_item_sensibili = df.lista_sensibili
            dataframe_bandizzato = df.dataframe_bandizzato
            QID = [x for x in dataframe_bandizzato.columns if x not in columns_item_sensibili]
            QID_list_to_select = list()
            for ii in range(kl_attempts):
                QID_select = list()
                while len(QID_select) < r:
                    temp = random.choice(QID)
                    if temp not in QID_select:
                        QID_select.append(temp)
                QID_list_to_select.append(QID_select)

            KLs = list()
            time_list = list()
            q_time_list = list()
            exit_list = list()

            for iii in range(q_value_attempts):
                start_time = time.time()
                q_value = np.random.uniform(min_q, max_q)
                cahd = CAHDalgorithm.CAHDalgorithm(
                    df,
                    grado_privacy=grado_privacy,
                    alfa=alpha,
                    q_value=q_value)
                cahd.compute_hist()
                hist_item = cahd.hist
                if cahd.CAHD_algorithm(analysis=True, plot=False):
                    end_time_1 = time.time() - start_time
                    KL_Divergence = 0
                    for ii in range(kl_attempts):
                        all_value = KLDivergence.get_all_combination_of_n(r)
                        # get max value of sensibile data
                        item_sensibile = int(max(hist_item.keys(), key=(lambda k: hist_item[k])))
                        QID_select = QID_list_to_select[ii]
                        for valori in all_value:
                            actsc = KLDivergence.compute_act_s_in_c(dataframe_bandizzato, QID_select, valori,
                                                                    item_sensibile)
                            estsc = KLDivergence.compute_est_s_in_c(dataframe_bandizzato, cahd.sd_gruppi,
                                                                    cahd.lista_gruppi,
                                                                    QID_select, valori, item_sensibile)
                            # print("est", estsc)
                            if actsc > 0 and estsc > 0:
                                temp = actsc * np.log(actsc / estsc)
                            else:
                                temp = 0
                            # print("KL_Divergence i = ", temp )
                            KL_Divergence += temp
                    KLs.append(KL_Divergence / kl_attempts)
                    ac_t = time.time()
                    print("%.2f | Attempt : %s | Density : %s | Q index : %s | Execution CAHD : %.2f | Execution KL-D : %.2f" % (
                    ac_t - big_ben, i, dens1, q_value, end_time_1, ac_t - start_time))
                    exit_list.append(len(cahd.lista_gruppi))
                else:
                    KLs.append(99999)
                    ac_t = time.time()
                    print("%.2f | Attempt : %s | Q index : %s | CAHD failed : %.2f" % (
                    ac_t - big_ben, i, iii, ac_t - start_time))
                    exit_list.append(-1)
                q_time_list.append(q_value)
                time_list.append(ac_t - start_time)
            name_file = nameFile.split("/")[1].split(".")[0] + "-" + str(num_sensibile) + "-" + str(
                grado_privacy) + "-" + str(kl_attempts) + "-" + str(r) + "-" + str(dim_finale)
            file_1 = open("Q-Study/" + name_file + "-divergence.txt", "a")
            file_3 = open("Q-Study/" + name_file + "-time.txt", "a")
            file_4 = open("Q-Study/" + name_file + "-exit.txt", "a")
            file_5 = open("Q-Study/" + name_file + "-input.txt", "a")
            for j in range(len(KLs)):
                file_1.write(str(KLs[j]) + ";")
                file_3.write(str(time_list[j]) + ";")
                file_4.write(str(exit_list[j]) + ";")
                file_5.write(str(q_time_list[j]) + "," + str(df.density) + ";")
            file_1.close()
            file_3.close()
            file_4.close()
            file_5.close()
