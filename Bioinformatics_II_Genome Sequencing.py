from textwrap3 import wrap


def entrada_manual():
    n = int(input('numero de entradas: '))
    lista = []
    print('\n entradas ')
    for i in range(n):
        string = input()
        lista.append(string)
    return lista

def lista_entrada(string, k):
    patterns = []
    for i in range(len(string) - k+1):
        #print(string[i:i + k])
        patterns.append(string[i:i + k])
    return patterns

'''
funcion para buscar las cadenas que son iguales en sufijo y prefijo, comparando
todas las subcadenasa. 
Entrada: una lista de k-mears.
Salida: el k-1mer y su k-1mer que es igual 
'''
# ----------------------------------------------------------------------------------------------------------------------

def prefijo_sufijo(kmers, k=5):
    print('\n')
    salida = {}
    for mer in sorted(set(kmers)):
        nodo1 = mer[:-1]
        salida[nodo1] = []
        for submer in kmers:
            subnodo1 = submer[:-1]
            subnodo2 = submer[1:]
            if(nodo1 == subnodo1):
                salida[nodo1].append(subnodo2)
                salida[nodo1] = sorted(salida[nodo1])
    for i in salida:
        print(i,'->',','.join(salida[i]))
    return salida
#prefijo_sufijo(['GAGG', 'CAGG', 'GGGG', 'GGGA', 'CAGG', 'AGGG', 'GGAG'])
#prefijo_sufijo(entrada_manual())

def Brujin_path(string, k):
    #k = 4
    #string = 'AAGATTCTCTAAGA'
    #kmers = lista_entrada(string, k)
    print(string)
    prefijo_sufijo(string, k)
#Brujin_path()

def camino_hamilton(kmers):
    r = ''
    match = prefijo_sufijo(kmers)
    for i in match:
        r += (i[:-1]+match[i][0][-1:])
    print(r)
    return 0
#camino_hamilton(entrada_manual())
#camino_hamilton(['ACCGA', 'CCGAA', 'CGAAG', 'GAAGC', 'AAGCT'])

# ----------------------------------------------------------------------------------------------------------------------
def ciclo_euleriano(inicio, grafo):
    nodo_actual = inicio
    ciclo = []
    while( ciclo.count(nodo_actual) != 1 ):                                     # cuando encuentre el inicio se termina el loop
        ciclo.append(nodo_actual)
        vecinos = grafo[nodo_actual]
        nodo_actual = vecinos.pop(-1)         # el ultimo vecino de la lista es el nodo a buscar. INVESTIGAR COMO SE ELIGE EL VECINO
    ciclo.append(nodo_actual)
    return ciclo

def grados_vecinos(nodo, grafo):
    vecinos = []                                                                   # lista de cantidad de grados
    for vecino in grafo[nodo]:
        grado_vecino = grafo[vecino]
        vecinos.append(len(grado_vecino))
    return vecinos

def nodo_inicio(ultimo, grafo):
    posible = []
    for nodo in grafo:
        if len(grafo[nodo]) > 1:                                        # si el nodo tiene mas de 1 grado
            posible.append(nodo)                                        # es posible candidato a nodo de inicio
    if posible == []:                                                   # si no hay nodos candidatos
        for nodo in grafo:                                              # todos tienen grado 1
            if grafo[nodo] != []:
                posible.append(nodo)

    ciclo = {}
    for nodo in posible:
        grados = grados_vecinos(nodo, grafo)                             # grados de cada nodo
        ciclo[nodo] = sum(grados)                                        # el ultimo valor de la lista sera igual a la suma de sus grados
    valores = list(ciclo.values())
    if valores == []:
        return valores
    else:
        minimo = min(valores)                                            # buscando el nodo vecino con menor grado
        if(minimo ==1):                                                  # si el minimo es 1 no hay mas grados
            return ultimo
        else:
            for i in ciclo:
                if(ciclo[i] == minimo):                                  # si el valor de cada nodo de un ciclo es igual al minimo
                    inicio = i
            posible.pop(posible.index(inicio))                           # elimina el nodo elegido de la lista
            termino = posible
            return inicio

def camino_euleriano(grafo):
    ciclos = []
    camino = []
    a = True
    primero = []
    ultimo = ''
    while a == True:                                                # mientras no se cumpla la condicion
        inicio = nodo_inicio(ultimo, grafo)                         # nodo de inicio para un ciclo
        primero.append(inicio)                                      # lista de nodos iniciales
        ultimo = inicio
        if inicio != []:
            '''
            for i in grafo:
                print(i, '=', grafo[i])
            print('\n')
            '''
            ciclo_i = ciclo_euleriano(inicio, grafo)                # ciclo euleriano desde el nodo inicial
            #print(ciclo_i)
            ciclos.append(ciclo_i)
        else:
            a = False
    return primero, ciclos

def main(grafo):
    # entradas en formato de diccionario
    grafo_dict = {}
    for nodo in grafo:
        nodo_actual, nodo_vecino = nodo.split('->')
        grafo_dict[nodo_actual.strip()] = nodo_vecino.strip().split(',')
    # variables: primero. Representa los vertices en que inician los ciclos.
    #            ciclos. es una lista que contiene listas de los ciclos de cada nodo
    primero, ciclos = camino_euleriano(grafo_dict)
    final = []
    p = primero[0]
    for ciclo in ciclos:
        i = ciclo.index(p)
        final.append(ciclo[i+1:])
        p = ciclo[0]
    ciclos = '->'.join(sum(final, []))
    print(primero[0] + '->' +ciclos + '->' + primero[0])
    return 0

entrada = ['0 -> 3',
           '1 -> 0',
           '2 -> 1,6',
           '3 -> 2',
           '4 -> 2',
           '5 -> 4',
           '6 -> 5,8',
           '7 -> 9',
           '8 -> 7',
           '9 -> 6']
entrada2 =['CTTA','ACCA','TACC','GGCT','GCTT','TTAC']
#entrada2 =['CTTAACCATACCGGCTGCTTTTAC']
#Brujin_path(entrada2, 4)
#entrada = entrada_manual()
#main(entrada2)

from random import shuffle
from itertools import product
def k_universal(k):
    
    k = 9
    data = product('01', repeat=k)
    l_data = [''.join(value) for value in list(data)]
    print(l_data)
    shuffle(l_data)
    print(l_data)
#k_universal(8)


aminos = {"UUU":"F", "UUC":"F", "UUA":"L", "UUG":"L", "UCU":"S", "UCC":"S", "UCA":"S", "UCG":"S", "UAU":"Y", "UAC":"Y",
          "UAA":"STOP", "UAG":"STOP", "UGU":"C", "UGC":"C", "UGA":"STOP", "UGG":"W", "CUU":"L", "CUC":"L", "CUA":"L",
          "CUG":"L", "CCU":"P", "CCC":"P", "CCA":"P", "CCG":"P", "CAU":"H", "CAC":"H", "CAA":"Q", "CAG":"Q", "CGU":"R",
          "CGC":"R", "CGA":"R", "CGG":"R", "AUU":"I", "AUC":"I", "AUA":"I", "AUG":"M", "ACU":"T", "ACC":"T", "ACA":"T",
          "ACG":"T", "AAU":"N", "AAC":"N", "AAA":"K", "AAG":"K", "AGU":"S", "AGC":"S", "AGA":"R", "AGG":"R", "GUU":"V",
          "GUC":"V", "GUA":"V", "GUG":"V", "GCU":"A", "GCC":"A", "GCA":"A", "GCG":"A", "GAU":"D", "GAC":"D", "GAA":"E",
          "GAG":"E", "GGU":"G", "GGC":"G", "GGA":"G", "GGG":"G"}
def reverse_com(string):
    comp = {'A': 'T', 'C': 'G', 'T': 'A', 'G': 'C'}
    n_string = ''.join([comp[i] for i in string[::-1]])
    return n_string

def encode(genoma):
    reverse = reverse_com(genoma)
    seq = []
    seqR = []
    for i in range(0, len(genoma), 3):
        codon = genoma[i:i+3]
        codonR = reverse[i:i+3]

        if codon == 'STOP':
            break
        codon = codon.replace('T', 'U')  # transcripcion
        codonR = codonR.replace('T', 'U')

        seq.append(aminos[codon])
        seqR.append(aminos[codonR])

    print(''.join(seq))
    print(''.join(seqR))
    return ''.join(seq)
#gen = 'GAAACT'
#encode(gen)


# Theorical spectrum
masas = {'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114,
         'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186}
def Cyclospectrum(peptido):
    espectro = []
    for i in range(1, len(peptido)+1):
        for j in range(len(peptido)):
            if j+i > len(peptido):
                espectro.append(peptido[j:]+peptido[:i-len(peptido[j:])])
            else:
                espectro.append(peptido[j:j+i])
    Masas = [0]
    for i in espectro:
        total = 0
        for j in i:
            total += masas[j]
        Masas.append(total)
    Masas = sorted(Masas)[:-3]
    return Masas
#print(Cyclospectrum('NQEL'))

def LinearEspectrum(peptido):
    espectro = []
    for step in range(1, len(peptido)+1):
        for j in range(0, len(peptido)):
            subp = peptido[j:j+step]
            if subp not in espectro:
                espectro.append(subp)
    Masas = [0]
    for i in espectro:
        total = 0
        for j in i:
            total += masas[j]
        Masas.append(total)
    Masas  = sorted(Masas)[:len(peptido)*3+1]
    return Masas
#print(LinearEspectrum('NQEL'))

def LinearEspectrumN(n):
    return sum([i for i in range(1, n+1)])+1
#print(LinearEspectrumN(4))


AminoMasas = {57: 'G', 71: 'A', 87: 'S', 97: 'P', 99: 'V', 101: 'T', 103: 'C', 113:'I/L', 114: 'N', 115: 'D', 128: 'K/Q',
            129: 'E', 131: 'M', 137: 'H', 147: 'F', 156: 'R', 163: 'Y', 186: 'W'}
def CountingMass(Mass, masslist):
    if Mass == 0:
        return 1, masslist
    if Mass < 57:
        return 0, masslist
    if Mass in masslist:
        return masslist[Mass], masslist
    n = 0
    for i in AminoMasas:
        k, masslist = CountingMass(Mass - i, masslist)
        n += k
    masslist[Mass] = n
    return n, masslist
print(CountingMass(10, {})[0])

def CyclopeptideScoring(peptido, espectro_experimental):
    espectro_teorico = LinearEspectrum(peptido)
    inter = [i for i in espectro_teorico if i in espectro_experimental]
    print(inter)
    return len(inter)
#print(CyclopeptideScoring('NQEL', [0, 99, 113, 114, 128, 227, 257, 299, 355, 356, 370, 371, 484]))

def expanding(espectro, espectro_exp, N):
    if N < 10:
        for peptido in espectro:
            for i in peptido:
                if i in espectro_exp:
                    for masa in AminoMasas:
                        #if masa in espectro_exp and sum(peptido)+masa in espectro_exp:
                        peptido.append(masa)
                else:
                    break
        expanding(espectro, espectro_exp, N + 1)
    return espectro
espectro = [[i] for i in [0, 99, 113, 114, 128, 227, 257, 299, 355, 356, 370, 371, 484]]
a = expanding(espectro,  [99, 113, 128, 227, 257, 370, 371], 0)
for i in a:
    print(i)

def LeaderboardCyclopeptideSequencing(N, espectro_experimental):
    LeaderPeptide = []
    samples = expanding(espectro_experimental)
    return LeaderPeptide