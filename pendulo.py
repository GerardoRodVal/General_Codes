# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 16:26:41 2016

@author: MarioAdrian
"""
import matplotlib.pyplot as plt
import math

#Posicion actual del penndulo
Oi=.5

#Posicion anterior del pendulo 
Oi_1=.4

#Posicion futura del pendulo
Oim2=0

#Gravedad
gravedad=1

#Largo de la cuerda
largo=.3

#Tiempo transcurrido en cada intervalo
diferenciatiempo=.2

#Tiempo total transcurrido 
sumatiempo=0

#Listas para graficar 
lx=[]
ly=[]

### El numero de iteraciones 
###Dentro de este for se van a hacer las iteraciones 
for i in range (100):
    # Se suma e valor actual a la acumulacion de tiempo 
    sumatiempo+=diferenciatiempo

    #Se cambia el valor Oi_1 por el Oi
    Oi_1 = Oi
    
    #Se cambien el valor Oi por el valor Oim2
    Oi=Oim2
    
    #Se calcula el nuevo valor del angulo 
    Oim2 = ((-(gravedad*math.sin(Oi))/largo)*(diferenciatiempo**2)) + (2*Oi) - Oi_1
    
    lx.append(sumatiempo)
    ly.append(Oim2)
    
    print("Angulo = ",Oim2, "en el tiempo ",sumatiempo )
    
plt.plot(lx, ly, 'ro')
plt.margins(0.2)
plt.subplots_adjust(bottom=0.15)
plt.show()

    
    