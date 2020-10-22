N = int(input())
A = map( int, raw_input().split(' '))
pasos = 0
cont = 2

if( N==2 ):
    pasos += 1
    
while( cont<N ):
    if( A[cont]==0 ):
        cont += 2
        pasos += 1
    elif( A[cont]==1 ):
        cont += 1
        pasos += 1
    if( cont==(N-2) ):
        cont += 1
        pasos += 1
print pasos