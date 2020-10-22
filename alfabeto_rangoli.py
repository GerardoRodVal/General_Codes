letras = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q',
'r','s','t','u','v','w','x','y','z']
A = int(input())
let = letras[:A:]

cont = 1
cont2 = 1
Ncont = len(let)-1
Ncont2 = len(let)-1

for i in range(len(let)):
    j = i
    if( j > 1 ):
        j = 1
    print ((A-cont2)*"--")+'-'.join(let[::-1][:cont:])+'-'*j + '-'.join(let[::-1][:cont-1:][::-1])+((A-cont2)*"--")
    if( cont==len(let)):
        for i in range(len(let)):
            k = 1
            if( Ncont == 1 ):
                k = 0
            print ((A-Ncont2)*"--")+'-'.join(let[::-1][:Ncont:])+'-'*k + '-'.join(let[::-1][:Ncont-1:][::-1])+((A-Ncont2)*"--") 
            Ncont -= 1
            Ncont2 -= 1
            if( Ncont==0 ):
                break
    
    cont += 1
    cont2 += 1