import pandas as pd
import numpy as np
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.sparse import csr_matrix
import matplotlib.pylab as pltt
import math
import random

# definizione

class BandMatrixQ2:
    size = None
    size_after_RCM = None
    dataframe = None  # dataframe iniziale
    dataframe_bandizzato = None  # dataframe after RCM e square
    items_final = None  # lista di tutti i prodotti indicizzati con colonna
    lista_sensibili = None  # lista prodotti sensibili
    df_square_complete = None  # matrice transazioni completa
    original_band = None  # larghezza banda pre processing
    density = 0  # densità matrice
    band_after_rcm = None  # larghezza banda dopo processing

    # inizializzazione

    def __init__(self, nome_file=None):
        # lettura file .csv
        self.dataframe = pd.read_csv(nome_file, header=None, index_col=None)
        self.size = self.dataframe.shape[0]

    def compute_band_matrix(self, dim_finale=1000, QID_columns=None, lista_sensibili_column=None, lista_sensibili_r=None, density=0.03, plot=True, withRCM=True):
        """
            Metodo per la lettura da file del dataframe e
            per la creazione di una matrice bandizzata
            tramite algoritmo reverse_cuthill_mckee
        """

        density = math.sqrt(density)

        # lettura file e dimensionamento matrice
        original_dataset = self.dataframe
        if original_dataset is not None and lista_sensibili_r is not None and lista_sensibili_column is not None and QID_columns is not None:
            if len(original_dataset.columns) < dim_finale + len(lista_sensibili_column):
                choose = input(
                    "Non ci sono abbastanza colonne, vuoi cambiare il numero di colonne da %d a %d? [s/n] " % (
                        dim_finale, len(original_dataset.columns) - len(lista_sensibili_column)))
                if choose == "s":
                    dim_finale = len(original_dataset.columns) - len(lista_sensibili_column)
                else:
                    return

            if len(original_dataset) < dim_finale:
                choose = input(
                    "Non ci sono abbastanza righe, vuoi cambiare il numero di righe da %d a %d? [y/N] " % (
                        dim_finale, len(original_dataset)))
                if choose == "y":
                    dim_finale = len(original_dataset)
                else:
                    return

            self.size_after_RCM = dim_finale
            # permutazione randomica valori da inserire nella matrice banda
            lista_sensibili_row = list()
            indice_righe = 0
            while len(lista_sensibili_row) < dim_finale and len(lista_sensibili_row) < len(lista_sensibili_r):
                lista_sensibili_row.append(lista_sensibili_r[indice_righe])
                indice_righe += 1
            lista_QID_column = list()
            indice_righe = 0
            while len(lista_QID_column) < dim_finale and len(lista_QID_column) < len(QID_columns):
                lista_QID_column.append(QID_columns[indice_righe])
                indice_righe += 1

            total_col = list()
            for pip in lista_QID_column:
                total_col.append(pip)
            for pip in lista_sensibili_column:
                total_col.append(pip)
            items_final = dict(zip(total_col, total_col))

            df_sensitive = original_dataset.iloc[lista_sensibili_row][lista_sensibili_column]
            df_square = original_dataset.iloc[lista_sensibili_row][lista_QID_column]

            sum_for_columns = df_square[lista_QID_column].sum()
            sum_total = 0
            for sum_column in sum_for_columns:
                sum_total += sum_column
            density_before = sum_total / (dim_finale * dim_finale)

            """
            df1 = df_square.sample(frac=density, axis=0)
            df2 = df1.sample(frac=density, axis=1)
            df3 = pd.DataFrame(1, index=df2.index, columns=df2.columns)
            df_square.update(df3)
            """
            num_rows = int(density*dim_finale)
            random_column = np.random.permutation(QID_columns)[:num_rows]
            random_row = np.random.permutation(lista_sensibili_row)[:num_rows]
            df_square.update(pd.DataFrame(1, index=random_row, columns=random_column))

            sum_for_columns = df_square[lista_QID_column].sum()
            sum_total = 0
            for sum_column in sum_for_columns:
                sum_total += sum_column
            self.density = sum_total / (dim_finale * dim_finale)

            print("Density before : %s -- %s -- %s" % (density_before, self.density, density*density))

            if withRCM:
                # creazione matrice banda tramite riordine della matrice iniziale
                sparse = csr_matrix(df_square)
                order = reverse_cuthill_mckee(sparse)

                column_reordered = [df_square.columns[i] for i in order]
                df_square_band = df_square.iloc[order][column_reordered]
                df_sensitive_band = df_sensitive.iloc[order]

                final_df = pd.concat([df_square_band, df_sensitive_band], axis=1, join='inner')
                # calcolo larghezze di banda pre e post processing
                [i, j] = np.where(df_square == 1)
                bw = max(i - j) + max(j - i) + 1
                self.original_band = bw

                [i, j] = np.where(df_square_band == 1)
                bw1 = max(i - j) + max(j - i) + 1
                self.band_after_rcm = bw1

                # parametri per il plot delle matrici
                if plot:
                    f, (ax1, ax2) = pltt.subplots(1, 2, sharey=True)
                    ax1.spy(df_square, marker='.', markersize='3')
                    ax2.spy(df_square_band, marker='.', markersize='3')
                    pltt.show()
                    print("Bandwidth before RCM: ", bw)
                    print("Bandwidth after RCM", bw1)

                self.dataframe_bandizzato = final_df
                self.items_final = items_final
                self.lista_sensibili = lista_sensibili_column

            else:
                final_df = pd.concat([df_square, df_sensitive], axis=1, join='inner')

                [i, j] = np.where(self.df_square_complete == 1)
                bw = max(i - j) + max(j - i) + 1
                self.original_band = bw
                self.band_after_rcm = bw
                if plot:
                    print("Bandwidth before RCM: ", bw)

                self.dataframe_bandizzato = final_df
                self.items_final = items_final
                self.lista_sensibili = lista_sensibili_column
        else:
            print("Error 404: Dataset not found or file not found.")
