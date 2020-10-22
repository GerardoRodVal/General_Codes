import pandas as pd
import numpy as np


def KNN( datos, K ):        
    A = datos
    train = []                                              # Conjunto de entrenamiento
    test = []                                               # Conjunto de prueba

    for i in range(len(list(A.Age))):
        if( np.isnan(A.values[i][5]) == True ):             # Para cada valor nan en el columna 'Age'
            train.append( A.values[i] )                     # Agrega la fila al conjunto de entrenamiento
        else:
            test.append( A.values[i] )                      # Si son diferentes de  nan, agrega la fila al conjunto de prueba

    matriz = []                                             # matriz de valores y escalares
    for i in range(len(train)):
        dist = []
        for j in range(len(test)):        
            Vec = map(int,test[j] == train[i])              # Transformando la fila a 0 y 1, de los conjuntos
            Vec = [sum(Vec)]                                # Transformando a un escalar
            Vec.append(test[i][5])                          # Agregando valores existentes del conjunto de entrenamiento
            dist.append(Vec)
        matriz.append(dist)

    for i in range(len(matriz)):
        clase = sorted(matriz[i])[::-1][:K:]                # Elijiendo vectores de la matriz para K elementos
        for j in clase:
            print( clase[0][1] )

    print( len(train) )
    print( len(matriz)*7 )
    return True



A = pd.read_csv('titanic.csv', header = 0, encoding = 'Latin-1')
A.columns = ['ID', 'something','class', 'name', 'gender', 'age', 'Age', 'X', 'number', 'dollars', 'room', 'survivor']
print( KNN( A, int(input('ingresa los K vecinos:  '))) )