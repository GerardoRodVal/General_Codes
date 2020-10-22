import pandas as pd
import random as rd
from numpy import subtract as resta
from math import sqrt
from sklearn.preprocessing import normalize


# datos[ columnas ][ fila ]
# columna individuos
# fila atributos

#-------------------------------------- Generacion de Individuos --------------------------------------#

def generar( datos ):
    azar = rd.randrange(0,103)                                # eligiendo un individuo aleatorio

    valores = map( float, list(datos[ azar ][:-1:]) )
    individuo = normalize(  valores )                         # normalizando valores
    estado = datos[ azar ][2135]                              # Guardando el estado del individuo


    azar2 = rd.randrange(0,103)                               # eligiendo un individuo aleatorio
    valores2 = map( float, list(datos[ azar2 ][:-1:]) )
    individuo2 = normalize( valores2 )                         # normalizando valores del individuo
    estado2 = datos[ azar2 ][2135]                            # Guardando el estado del individuo

    individuo = individuo[0]
    individuo2 = individuo2[0]

    print
    print 'Ditancia Euclidea -------', Euclidea(individuo, individuo2)                     # Calculando distancia
    print 'Distancia Manhattan -----', Manhattan(individuo, individuo2)
    print 'Distancia Bray-Curtis ---', BrayCurtis(individuo, individuo2)
    print 'Distancia Canberra ------', Canberra(individuo, individuo2)
    print 'Distancia Coseno --------', Coseno(individuo, individuo2)
    return estado, estado2



#-------------------------------------- Distancias de Similitud --------------------------------------#


def Euclidea(instancia1, instancia2):
    similitud = sqrt( sum([ resta( i[0],i[1] )**2 for i in zip( instancia1, instancia2 ) ]) )
    return similitud

def Manhattan( instancia1, instancia2 ):
    similitud = sum([ abs(resta( i[0],i[1] )) for i in zip( instancia1, instancia2 ) ])
    return similitud

def BrayCurtis( instancia1, instancia2 ):
    similitud1 = sum([abs(resta(i[0], i[1])) for i in zip(instancia1, instancia2)])
    similitud2 = sum([ sum(i) for i in zip(instancia1, instancia2) ])
    similitud = similitud1 / similitud2
    return similitud

def Canberra( instancia1, instancia2 ):
    similitud = sum([ (abs(resta(i[0], i[1])) / sum(i))  for i in zip(instancia1, instancia2) ])
    return similitud

def Coseno( instancia1, instancia2 ):
    similitud1 = sum([ i[0]*i[1] for i in zip(instancia1, instancia2) ])
    similitud2 = sum([ i**2 for i in instancia1 ])
    similitud3 = sum([ i**2 for i in instancia2 ])
    similitud = similitud1 / sqrt((similitud2*similitud3))
    return similitud


#----------------------------------------------------------------------------------------------#


print generar( datos = pd.read_csv( 'C:\Users\Gerardo Rodriguez\Desktop\Mineria de Datos\prostate_preprocessed.txt', sep=" ", header = None ) )
