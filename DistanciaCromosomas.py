def distancia( par, inicial ):

    candidatos = []
    while( len(par) > 1 ):                          # condicion de paro
        for i in par:
            if( inicial in i[1] ):
                candidatos.append( i )

        if( candidatos[0][1][0] == inicial ):       # eligiendo candidado correcto
            inicial = candidatos[0][1][1]
        else:
            inicial = candidatos[0][1][0]

        print inicial, candidatos

        indice = par.index( candidatos[0] )         # eligiendo indice del candidado elegido
        par.pop( indice )                           # sacando el candidato de la lista

        if( inicial in orden ):                     # ordenando correctamente
            distancia(par, inicial)
        else:
            orden.append(inicial)
            distancia( par, inicial )

    return ''.join(orden)



orden = []
lista = []
for i in range(int(input('numero de entradas: '))):
    c,d = raw_input().split(' ')
    lista.append( (int(d),c) )

inicial = sorted(lista)[-1][1][0]              # definiendo letra actual
final = sorted(lista)[-1][1][1]
lista = sorted(lista)[:-1]
orden.append( inicial )
print distancia( sorted(lista), inicial )

'''         CBAD
AB 42
AC 25
AD 23
BC 15
CD 28
'''

'''         HBAG
HG 20
AH 18
AB 10
BH 8
AG 2
'''

'''         BCAD
BD 14
CD 12
AD 6
BC 2
AB 8
'''