#!/usr/bin/python

def serie( n ):
	if( n == 0 ):
		return 0
	elif( n == 1 ):
		return 1
	else: 
		return( serie(n-1) + serie(n-2) )

print( serie( int(input('Ingrese la posicion de fibonacci para calcular: ')) ) )