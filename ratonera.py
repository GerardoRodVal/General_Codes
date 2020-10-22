import numpy as np

print (' a) Cual es la probabilidad de que, dado el raton esta en una habitacion cambie a cada una de las otras?')

print (' b) si empieza en la habitacion A, cual es la probabilidad de que este en cada uno de otros cuartos en dos minutos? ')

print (' c) Cual es el cuarto que el raton pasara menos tiempo? ' )

print (' d) Dados dos cuartos del laberinto, Cual es la longitud del viaje mas corto? ')

print (' e) Dados dos cuartos del laberinto, Cuanto caminos conlongiutd minima hay entre ellos?')

A = np.matrix( ( (0,1.0/2,0,0,0,1.0/2) , (1.0/3,0,0,1.0/3,0,1.0/3) , (0,0,0,1,0,0) , (0,1.0/3,1.0/3,0,1.0/3,0) , (0,0,0,1.0/2,0,1.0/2) , (1.0/3,1.0/3,0,0,1.0/3,0) ) )
print(A)
In = input( 'ingrese solo la letra del inciso a resolver:  ' )
if( In == 'a' ):
    print (A)
    
elif( In == 'b' ):
    print (A**2,(A**2)[0])
    
elif( In == 'c' ):
    potencia = 1
    fin = 0
    
    while( fin != 1 ):
        A = A**potencia
        columnas = []
        cont = 0 
        for i in range(len(A)): #sacando los valores de las columnas
            lista = []
            cont2 = 0  
            for j in range(len(A)):
                lista.append(int(A[cont2,cont]*100)) #calculando los primeros decimales
                cont2 += 1
            cont += 1
            columnas.append(lista)
        C = [str(sum(i)/6).split('.')[1] == '0' for i in columnas] #calculando la suma de las columnas
        if(set(C)=={True}): #verificando que todos los decimales sean iguales
            fin = 1
        potencia += 1
    print(A)
    cuartos = {}        
    cuartos['a'] = columnas[0][0]
    cuartos['b'] = columnas[1][0]
    cuartos['c'] = columnas[2][0]
    cuartos['d'] = columnas[3][0]
    cuartos['e'] = columnas[4][0]
    cuartos['f'] = columnas[5][0]
    cua = list(cuartos.items())
    cua.sort(key=lambda x: x[1])
    print ("cuarto que pasara menos tiempo: ",cua[0][0])
    
elif(In == 'd' or 'e'):
	a = input('cuarto 1: ')
	b = input('cuarto 2: ')
	matriz = np.matrix( ( (0,1,0,0,0,1) , (1,0,0,1,0,1) , (0,0,0,1,0,0) , (0,1,1,0,1,0) , (0,0,0,1,0,1) , (1,1,0,0,1,0) ) )
	Mat = matriz
    pasos = 1
    final = 0
	while( final != 0 ):
		if( matriz[a,b] != 0 ):
			print(matriz[a,b], pasos)
		else: 
			pasos += 1
			Mat = matriz * Mat

    print(matriz(a,b))
        
        
    
    
    
    
    