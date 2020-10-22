import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames

dataset = pd.read_csv( '/home/gerardo/Documentos/knotion/github/inegi-data/data/socioeconomicos_manzana_nonan.csv', nrows = 500)                                       # Archivo de entrada
N_Clusters = 5                                                                                                          # Numero de clusters

Columnas = dataset.columns[11:]                                                                                         # Columnas para procesar

Random_columnas = [ rd.choice( Columnas ) for i in range(3) ]

X = np.array(dataset[Random_columnas])
y = np.array(dataset[ rd.choice( list(dataset) ) ])

k_means = KMeans(n_clusters=N_Clusters).fit(X)  # Aplicando algoritmo Kmeans a las columnas elegidas
centroides = k_means.cluster_centers_  # Generando clusters
clases = k_means.predict(X)  # Calculando la prediccion de clases
colores = [rd.choice(list(cnames)) for i in range(N_Clusters) ]                                                         # Eligiendo colores aleatorios
asignar=[]
for row in clases:                                                                                                      # Asiganando un color a cada clase
    asignar.append(colores[row])

for i in range(6):
    C_clusters = k_means.cluster_centers_                                                                                   # Calculando los nuevos clusters

    fig = plt.figure()                                                                                                      # Graficando clases
    ax = Axes3D(fig)
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=asignar,s=60)
    ax.scatter(C_clusters[:, 0], C_clusters[:, 1], C_clusters[:, 2], marker='*', c=colores, s=1000)

    plt.show()

dataset['clase'] = clases                                                                                               # Agregando columna de clase al conjunto
dataset.to_csv( './Kmeans_Automatico_Salida.csv' )                                                                      # Guardando archivo
