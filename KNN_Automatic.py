import matplotlib.pyplot as plt
import pandas as pd
import random as rd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.datasets import load_breast_cancer

def KNN ( dataset, K ):
    print( zdataset )

    print( "\n RESUMEN DEL CONJUNTO \n\n", X.describe() )
    X = X[ rd.choice( dataset.columns ) ]
    print( X )
    X = X[['mean area', 'mean compactness']]                                            # Datos filtrados a las columnas 'mean area' y 'mean compactness'
    print( dataset.target )
    print( dataset.target_names )
    y = pd.Categorical.from_codes(dataset.target, dataset.target_names)                 # Ajustando etiquetas a sus nombres
    y = pd.get_dummies(y, drop_first=True)                                              # convierte variables categoricas en indicadoras

    ''' conjunto X de entrenamiento y prueba se divide complementariamente del conjnuto
        Conjunto Y de entrenamiento y prueba usados de las etiquetas y sus variables'''

    X_train, X_test, Y_train, Y_test = train_test_split(X, y)                           # Divide los conjuntos de entrenamiento y prueba

    knn = KNeighborsClassifier(n_neighbors = K, metric='euclidean')                      # Configurando KNN
    knn.fit(X_train, Y_train)                                                           # Aplicando la funcion KNN

    print('\n Precision de KNN en el conjunto de entrenamiento : {:.2f}'.format(knn.score(X_train, Y_train)))
    print('\n Precision de KNN en el conjunto de prueba: {:.2f}'.format(knn.score(X_test, Y_test)))

    y_pred = knn.predict(X_test)                                                        # Conjunto clasificacion

    plt.scatter(                                                                        # Graficando resultados
        X_test['mean area'],
        X_test['mean compactness'],
        c=y_pred,
        cmap='coolwarm',    # --------------------------- Dividiendo conjuntos de entrenamiento y prueba ---------------------------------

        alpha=0.6
    )
    print( "\n MATRIZ DE CONFUSION \n\n", confusion_matrix(Y_test, y_pred) )
    print( "\n REPORTE DE CLASIFICACION \n\n", classification_report(Y_test, y_pred) )
    plt.show()

dataset = load_breast_cancer()                                                          # Datos precargados en modulo
K = 10
KNN( dataset, K )






'''
Matriz de confusion. Permite la visualizacion de desempeño del algortimo.
De 8 gatos, se predijeron 3 como perro y 0 conejos.

          Valor Predicho
       Gato  Perro Conejo
Gato	 5	  3      0
Perro	 2	  3      1
Conejo   0    2	    11
'''