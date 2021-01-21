import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import preprocessing
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames

def kmeans():
    '''
    1. Seleccionar el número de k grupos (clusters)
    2. Generar aleatoriamente k puntos que llamaremos centroides
    3. Asignar cada elemento del conjunto de datos al centroide más cercano para formar k grupos
    4. Reasignar la posición de cada centroide
    5. Reasignar los elementos de datos al centroide más cercano nuevamente
       5.1 Si hubo elementos que se asignaron a un centroide distinto al original, regresar al paso 4, de lo contrario, el proceso ha terminado
    '''

    dataset = pd.read_csv('files/titanic.csv')

    '''preprocesando datos'''
    print(dataset.columns) # elegir dos columnas
    columns = ['Age', 'Fare']
    dataset[columns].fillna(np.mean(dataset[columns]), inplace=True)
    dataset[columns] = preprocessing.scale(dataset[columns])

    X = dataset[columns[0]]
    Y = dataset[columns[1]]
    plt.plot(X,Y, 'o')
    #plt.show()

    '''Eligiendo los centroides'''
    k = 2
    centroid_list = []
    for i in range(k):
        Centroids = {}
        randomCentriod = rd.randrange(0, dataset.shape[0])                                                              # eligiendo un valor centroide aleatorio
        for col in columns:
            Centroids[col] = dataset.iloc[randomCentriod][col]
        centroid_list.append(Centroids)

    '''calculando las distancia de cada punto a cada centroide'''
    max_iter = 7
    iters = 0
    cluster_train = []
    while iters < max_iter:
        for i in range(dataset.shape[0]):                                                                               # para cada valor de mi conjunto
            cluster_index = 0
            mini = 9999
            for centroid in centroid_list:                                                                              # para cada centroide
                centr_values = list(centroid.values())
                data_values = list(dataset[columns].iloc[i])
                dist = np.linalg.norm([centr_values[0]-data_values[0], centr_values[1]-data_values[1]])
                if dist < mini:
                    mini = dist
                    cluster_train[i] = cluster_index
            cluster_index += 1

        ''''''
        for ind in range(len(centroid_list)):
            SumCentroidPt = {}
            count = 0
            for col in columns:
                SumCentroidPt[col] = 0
            for i in range(dataset.shape[0]):
                if (cluster_train[i] == ind):
                    count = count + 1
                    for col in columns:
                        SumCentroidPt[col] = SumCentroidPt[col] + dataset.iloc[i][col]

        for col in columns:
            SumCentroidPt[col] = SumCentroidPt[col] / count
        centroid_list[ind] = SumCentroidPt

    iters += 1





    k_means = KMeans(n_clusters=k).fit(X)
    centroides = k_means.cluster_centers_
    clases = k_means.predict(X)

    colores = [rd.choice(list(cnames)) for i in range(k)]

    asignar = []
    for row in clases:  # Asiganando un color a cada clase
        asignar.append(colores[row])

    for i in range(6):
        C_clusters = k_means.cluster_centers_  # Calculando los nuevos clusters

        fig = plt.figure()  # Graficando clases
        ax = Axes3D(fig)
        ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=asignar, s=60)
        ax.scatter(C_clusters[:, 0], C_clusters[:, 1], C_clusters[:, 2], marker='*', c=colores, s=1000)

        plt.show()

        dataset['clase'] = clases  # Agregando columna de clase al conjunto
        dataset.to_csv('./Kmeans_Automatico_Salida.csv')

kmeans()