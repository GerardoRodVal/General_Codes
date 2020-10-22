import numpy as np                                  # Graficar numpy o pyllow
import matplotlib.pyplot as plt
from textwrap import wrap as wp

def Dot_plot_1( sec1, sec2 ):                       # Graficando secuencia de ventana 1
    M = []
    for i in sec1:                                  # hacuendo comparacion entre secuencias
        fila = []
        for j in sec2:                              # secuencia 2
            if( i == j ):                           # creando matriz binomial con lugares iguales
                fila.append(1)
            else:
                fila.append(0)
        M.append(fila)
    Matriz = np.matrix( M )
    plt.autoscale()
    plt.xticks(range(len(sec2)),sec2)
    plt.yticks(range(len(sec1)),sec1)
    plt.imshow( Matriz, cmap=plt.cm.gray_r )
    plt.savefig('Dot_plot_1.png')
    plt.show()
    return 'OK para Dot-plot 1'

def Dot_plot_3( sec1, sec2 ):                         # Graficando secuencia de ventana 3
    sec1 = wp(sec1,3)
    sec2 = wp(sec2,3)
    M = []
    for i in sec1:                                  # hacuendo comparacion entre secuencias
        fila = []
        for j in sec2:                              # secuencia 2
            if( i == j ):                           # creando matriz binomial con lugares iguales
                fila.append(1)
            else:
                fila.append(0)
        M.append(fila)
    Matriz = np.matrix( M )                          # Haciendo nuestras listas vectores
    plt.autoscale()
    plt.xticks(range(len(sec2)),sec2,rotation=90)       # definiendo tecto de eje X
    plt.yticks(range(len(sec1)),sec1)                   # definiendo texto de eje y
    plt.imshow( Matriz, cmap=plt.cm.gray_r )
    plt.savefig('Dot_plot_3.png')
    plt.show()
    return 'OK para Dot-plot 3'


a = input('Ingresa la secuencia 1:  ')
b = input('Ingresa la secuencia 2:  ')
print(Dot_plot_1(a.lower(), b.lower()))
print(Dot_plot_3(a.lower(), b.lower()))


# MTMDKSELVQKAKLAEQAERYDDMAAAMKAVTEQGHELSNEERNLLSVAYKNVVGARRSSWRVISSIEQKTERNEKKQQMGKEYREKIEAELQDICNDVLELLDKYLIPNATQPESKVFYLKMKGDYFRYLSEVASGDNKQTTVSNSQQAYQEAFEISKKEMQPTHPIRLGLALNFSVFYYEILNSPEKACSLAKTAFDEAIAELDTLNEESYKDSTLIMQLLRDNLTLWTSENQGDEGDAGEGEN
# RKPLQTPTPIRRLWTMDTSELVQKAKLAEQAERYDDMAASMKAVTEQGAELSNEERNLLSVAYKNVVGARRSSWRVISSIEQKTEGSEQKQQMAREYREKIEAELRDICNDVLGLLDKYLIANASKAESKVFYLKMKGDYYRYLAEVAAGEDKKSTVDHSQQVYQEAFEISKKEMTSTHPIRLGLALNFSVFYYEILNLPEQACGLAKTAFDDAISELDKLGDESYKDSTLIMQLLRDNLTVST