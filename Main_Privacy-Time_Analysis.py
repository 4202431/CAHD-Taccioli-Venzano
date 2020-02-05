import getopt
import sys

import BandMatrix
import CAHDalgorithm
import time

if __name__ == "__main__":
    dim_finale = 1000
    num_sensibile = 10
    grado_privacy_list = [4, 6, 8, 10, 16, 20]
    name_file_list = ["Dataset/BMS1.csv"]
    list_item = ["Dataset/Items_BMS1.txt"]
    alpha = 3
    max_attempts = 40

    # controllo gli eventuali argomenti di command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:i:n:m:p:x:",
                                   ["dataset=", "items=", "n=", "m=", "p=", "maxattempts="])
    except getopt.GetoptError:
        print('Main_Privacy-Time_Analysis.py \n' +
              ' -d <path dei dataset, intervallati da virgola>\n' +
              ' -i <path dei file con i codici prodotti, intervallati da virgola>\n' +
              ' -n <dimensione matrice quadrata>\n' +
              ' -m <numero attributi sensibili>\n' +
              ' -p <gradi di privacy, intervallati da virgola>\n' +
              ' -x <numero di ripetizioni>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Main_Privacy-Time_Analysis.py \n' +
                  ' -d <path dei dataset, intervallati da virgola>\n' +
                  ' -i <path dei file con i codici prodotti, intervallati da virgola>\n' +
                  ' -n <dimensione matrice quadrata>\n' +
                  ' -m <numero attributi sensibili>\n' +
                  ' -p <gradi di privacy, intervallati da virgola>\n' +
                  ' -x <numero di ripetizioni>')
            sys.exit()
        elif opt in ("-d", "--dataset"):
            name_file_list = arg.split(",")
        elif opt in ("-i", "--items"):
            list_item = arg.split(",")
        elif opt in ("-n", "--n"):
            dim_finale = int(arg)
        elif opt in ("-p", "--p"):
            input_array = arg.split(",")
            grado_privacy_list = [int(x) for x in input_array]
        elif opt in ("-m", "--m"):
            num_sensibile = int(arg)
        elif opt in ("-x", "--maxattempts"):
            max_attempts = int(arg)

    for index_nameFile in range(len(name_file_list)):
        big_ben = time.time()
        nameFile = name_file_list[index_nameFile]
        df = BandMatrix.BandMatrix(nameFile)
        listaItem = list_item[index_nameFile]
        for att in range(max_attempts):
            for i in range(2):
                for index_grado_privacy in range(len(grado_privacy_list)):
                    start_time = time.time()
                    print("%.2f |File : %s | Mode : %s | Attempt : %s | Index privacy: %s" % (start_time - big_ben, index_nameFile, i, att, index_grado_privacy))

                    name_file = nameFile.split("/")[1].split(".")[0] + "-" + str(dim_finale) + "-" + str(num_sensibile)

                    withRCM = (i != 0)

                    df.compute_band_matrix(
                        dim_finale=dim_finale,
                        nome_file_item=listaItem,
                        num_sensibile=num_sensibile,
                        plot=False,
                        withRCM=withRCM)
                    dataframe_bandizzato = df.dataframe_bandizzato.copy()

                    grado_privacy = grado_privacy_list[index_grado_privacy]
                    cahd = CAHDalgorithm.CAHDalgorithm(
                        df,
                        grado_privacy=grado_privacy,
                        alfa=alpha)
                    cahd.compute_hist()
                    hist_item = cahd.hist
                    if(cahd.CAHD_algorithm(analysis=True,
                                           plot=False)):
                        end_time = time.time() - start_time
                        file_1 = open("MainPlotData/3/" + name_file + ".txt", "a")
                        file_1.write(str(i) + "," + str(grado_privacy) + "," + str(end_time) + ";")
                        file_1.close()
