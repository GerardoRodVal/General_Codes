
def PatternCount( Text, Pattern):                                                                              # funcion para contar una palabra en un string
    count = 0                                                                                                       # contador de patrones
    for i in range(len(Text)-len(Pattern)+1):                                                                       # Buscando patrones parecidos en Text
        if Text[i:i+len(Pattern)] == Pattern:                                                                       # si el subconjunto es igual al patron
            count = count+1
    return count

def FrequencyMap( Text, k):                                                                                    # funcion para buscar subconjuntos de longitud k en un texto
    freq = {}                                                                                                       # patrones con su cardinalidad
    for i in range(len(Text)-k+1):
        Pattern = Text[i:i+k]                                                                                       # Patron igual al subconjunto de longitud k de Text
        count = PatternCount(Text, Pattern)                                                                    # Busca cuantos patrones iguales al subconjunto hay
        freq[Pattern] = count                                                                                       # guarda el patron y su cardinalidad
    return freq

def FrequentWords( Text, k):
    words = []
    freq = FrequencyMap(Text, k)                                                                               # Resultado de patrones y su cardinalidad
    m = max(freq.values())                                                                                          # patron con mas frecuencia
    for key in freq:                                                                                                # iterando sobre cada patron
        if(freq[key]==m):                                                                                           # si el patron tiene cardinalidad igual a la maxima
            words.append(key)                                                                                       # guardando
    return words

def SymbolArray( Genome, symbol):                                                                              # funcion para contar cada base nitronegada por indice
    array = {}
    n = len(Genome)
    ExtendedGenome = Genome + Genome[0:n//2]
    for i in range(n):
        array[i] = PatternCount(ExtendedGenome[i:i + (n // 2)], symbol)
    return array

def SkewArray( Genome):                                                                                        # funcion para contar la diferencia de apariciones de una base con otra
    skew = [0]
    score = {"A": 0, "T": 0, "C": -1, "G": 1}                                                                       # pesos dados a cada base
    for i in range(1, len(Genome) + 1):
        skew.append(score[Genome[i - 1]] + skew[i - 1])                                                             # sumando con los pesos anteriores
    return skew

def HammingDistance( p, q):                                                                                    # la distacia hamming es la cantidad de letras diferentes en el gen p y q
    return len([i for i in zip(p, q) if i[0] != i[1]])

def ApproximatePatternMatching( Text, Pattern, d):                                                             # funcion para calcular la distancia hamming de todos los subconjuntos de un text dado un patron
    positions = []
    q = Pattern
    for i in range(len(Text) - len(Pattern) + 1):                                                                   # recorriendo el text para cada subconjunto que inicia en i
        p = Text[i:i + len(Pattern)]                                                                                # subconjuntos
        if HammingDistance(p, q) <= d:                                                                         # subconjunto de al menos d distancia hamming
            positions.append(i)
    return positions

def Count( Motif):                                                                                             # ---- FUNCION PARA DETERMINAR LA FRECUENCIA DE NUCLEOTIDOS EN UN CADA POSICION
    count = {}                                                                                                      # formato de entrada: matriz, lista de listas
    M = len(Motif[0])                                                                                               # primer elemento de la lista
    N = len(Motif)
    for symbol in 'ACGT':
        count[symbol] = [0 for i in range(len(Motif[0]))]                                                           # agregando cada letra al diccionario de listas

    for i in range(N):                                                                                              # para cada fila
        for j in range(M):                                                                                          # para cada columna
            symbol = Motif[i][j]                                                                                    # cada elemento por fila
            count[symbol][j] += 1                                                                                   # suma por cada posicion
    return count

def Consensus(Motifs):                                                                                        # FUNCION PARA ENCONTRAR LA SECUENCIA CONSENSO
    k = len(Motifs[0])
    count = Count(Motifs)                                                                                           # calculando la frecuencia de las letras en su posicion
    consensus = ""
    for j in range(k):
        m = 0
        frequentSymbol = ""
        for symbol in "ACGT":
            if count[symbol][j] > m:
                m = count[symbol][j]
                frequentSymbol = symbol
        consensus += frequentSymbol
    return consensus

def Score(Motifs):                                                                                                      # FUNCION PARA MEDIR CUANTAS LETRAS SON IGUAL ENTRE LA SECUENCIA CONSENSO Y CADA ELEMENTO DEL MOTIF
    score = 0
    for i in Motifs:
        for j,k in zip(Consensus(Motifs),i):
            if j == k:
                score += 0
            else:
                score += 1
    return score-1
#print('salida score:', Score(['GGCCGGTT', 'AATTTGCG', 'AATCCGAG', 'CAAATCGC', 'GGATACAA']))

def Profile(Motifs):                                                                                                    # FUNCION PARA ENCONTRAR LA MATRIZ PERFIL DE MOTIFS
    count = {}                                                                                                          # matriz de cantidad de bases ACGT que hay por columna
    M = len(Motifs[0])                                                                                                  # diviido en la longitud de cada secuencia
    N = len(Motifs)
    for symbol in 'ACGT':
        count[symbol] = [0 for i in range(len(Motifs[0]))]
    for i in range(N):
        for j in range(M):
            symbol = Motifs[i][j]
            count[symbol][j] += 1/N
    return count
#print('salida:', Profile(['GGCCGGTT', 'AATTTGCG', 'AATCCGAG', 'CAAATCGC', 'GGATACAA']))

def Pr(Text, Profile):                                                                                                  # ENCONTRAR LA PROBABILIDAD DE LA CADENA DE ENTRADA, SEGUN SU POSICION DE BASE CON LA PROBABILIDAD DE LA MATRIZ PERFIL
    p = 1                                                                                                               # Entrada: diccionario de matriz profile. orden de llaves: 'ACGT'
    for pos, i in enumerate(Text):
        p *= Profile[i][pos]
    return p
#print(Pr('AGAATCTA', {'A': [0.4, 0.6000000000000001, 0.4, 0.2, 0.2, 0, 0.4, 0.2], 'C': [0.2, 0, 0.2, 0.4, 0.2, 0.4, 0.2, 0.2], 'G': [0.4, 0.4, 0, 0, 0.2, 0.6000000000000001, 0.2, 0.4], 'T': [0, 0, 0.4, 0.4, 0.4, 0, 0.2, 0.2]}))

def ProfileMostProbableKmer(text, k, profile):                                                                          # K-MERO MAS PROBABLE DENTRO DE UNA SECUENCIA SEGUN LA MATRIZ DE PROBABILDIADES PROFILE
    n = len(text)
    pr = {}
    most_prob_kmer = []
    for i in range(n-k+1):
        k_mer = text[i:i+k]                                                                                             # iterando sobre cada subcadena de longitud k
        probability = Pr(k_mer, profile)                                                                                # calculando la probabilidad de la subcadena
        pr[k_mer] = probability                                                                                         # guardando en diccionario la probabilidad de cada subcadena
    m = max(pr.values())
    for key, value in pr.items():                                                                                       # iterando sobre las llaves y valores del diccionario de probabilidades
        if pr[key] == m:                                                                                                # si el valor de una llave es igual al valor maximo
            most_prob_kmer.append(key)                                                                                  # guarda el valo de la llave
    return most_prob_kmer
#print(ProfileMostProbableKmer('AGAATCTA',7,{'A': [0.4, 0.6000000000000001, 0.4, 0.2, 0.2, 0, 0.4, 0.2], 'C': [0.2, 0, 0.2, 0.4, 0.2, 0.4, 0.2, 0.2], 'G': [0.4, 0.4, 0, 0, 0.2, 0.6000000000000001, 0.2, 0.4], 'T': [0, 0, 0.4, 0.4, 0.4, 0, 0.2, 0.2]}))


def ProfileMostProbablePattern(text,k,profile):                                                                         # PATRON MAS PROBABLE DENTRO DE UNA SECUENCIA SEGUN LA MATRIZ DE PROBABILIDAD PROFILE
    p=-1
    result=''
    for i in range(len(text)-k+1):
        seq=text[i:i+k]                                                                                                 # iterando sobre cada subcadena de longitud k en la secuencia de entrada
        pr=Pr(seq,profile)                                                                                              # probabilidad de la subcadena segun la matriz profile
        if pr>p:                                                                                                        # obteniendo la probabilidad mas grande
            p=pr
            result=seq
    return result
#print(ProfileMostProbablePattern('AGAATCTATCTGATGAATCT',3,{'A': [0.4, 0.6000000000000001, 0.4, 0.2, 0.2, 0, 0.4, 0.2], 'C': [0.2, 0, 0.2, 0.4, 0.2, 0.4, 0.2, 0.2], 'G': [0.4, 0.4, 0, 0, 0.2, 0.6000000000000001, 0.2, 0.4], 'T': [0, 0, 0.4, 0.4, 0.4, 0, 0.2, 0.2]}))

def GreedyMotifSearch(Dna, k, t):
    BestMotifs = []
    for i in range(0, t):
        BestMotifs.append(Dna[i][0:k])
    n = len(Dna[0])
    for i in range(n-k+1):
        Motifs = []
        Motifs.append(Dna[0][i:i+k])
        for j in range(1, t):
            P = Profile(Motifs[0:j])
            Motifs.append(ProfileMostProbablePattern(Dna[j], k, P))
        if Score(Motifs) < Score(BestMotifs):
                BestMotifs = Motifs
    return BestMotifs
print(GreedyMotifSearch([['ACGTGA'], ['ACGTGA'], ['AACCGT'], ['TTAGCT']], 2,3))

import math
def entropy():
    profile = [0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.9, 0.1, 0.1, 0.1, 0.3, 0.0, 0.1, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.1, 0.2, 0.4, 0.6, 0.0, 0.0, 1.0, 1.0, 0.9, 0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0,0.7, 0.2, 0.0, 0.0, 0.1, 0.1, 0.0, 0.5, 0.8, 0.7, 0.3, 0.4]
    entropy=0
    for item in profile:
        if item==0:
            del item
        else:
            entropy += -(item*math.log(item,2))
    return entropy

import random
def GibbsSampler(Dna, k, t, N):
    BestMotifs = []
    Motifs = RandomMotifs(Dna, k, t)
    BestMotifs = Motifs
    for j in range(1,N):
        i = random.randint(0,t-1)
        ReducedMotifs = []
        for j in range(0,t):
            if j != i:
                ReducedMotifs.append(Motifs[j])
        Profile = ProfileWithPseudocounts(ReducedMotifs)
        Motif_i = ProfileGeneratedString(Dna[i], Profile, k)
        Motifs[i] = Motif_i
        if Score(Motifs) < Score(BestMotifs):
                BestMotifs=Motifs
    return BestMotifs

def RandomMotifs(Dna, k, t):
    s = len(Dna[0])
    rm = []
    for i in range(0,t):
        init_index = random.randint(1,s-k)
        rm.append(Dna[i][init_index:init_index+k])
    return rm

def ProfileWithPseudocounts(Motifs):
    t = len(Motifs)
    k = len(Motifs[0])
    profile = {}
    c = CountWithPseudocounts(Motifs)
    for n in 'ACGT':
        p = []
        for i in range(0,k):
            p.append(c[n][i]/(t+4))
        profile[n] = p
    return profile

def CountWithPseudocounts(Motifs):
    t = len(Motifs)
    k = len(Motifs[0])
    count = {}
    for symbol in "ACGT":
        count[symbol] = []
        for j in range(k):
             count[symbol].append(1)
    for i in range(t):
        for j in range(k):
             symbol = Motifs[i][j]
             count[symbol][j] += 1
    return count

def testinterval(ar,r):
    ar.sort()
    if r<= ar[0]:
      return ar[0]
    for i in range(1,len(ar)-1):
      if ar[i-1]<r<=ar[i]:
        return ar[i]
    if ar[len(ar)-2]< r:
      return ar[len(ar)-1]

def WeightedDie(Probabilities):
    sumprob = {}
    s = 0
    for p in Probabilities:
        s += Probabilities[p]
        sumprob[p] = s
    revprob = {}
    for q in sumprob:
      revprob[sumprob[q]] = q
    w = list(sumprob.values())
    r = random.uniform(0,1)
    kmer = revprob[testinterval(w,r)]
    return kmer

def ProfileGeneratedString(Text, profile, k):
    n = len(Text)
    probabilities = {}
    for i in range(0,n-k+1):
        probabilities[Text[i:i+k]] = Pr(Text[i:i+k], profile)
    probabilities = Normalize(probabilities)
    return WeightedDie(probabilities)

def Pr(Text, Profile):
    # insert your code here
    p = 1
    for i in range(0,len(Text)):
        p *= Profile[Text[i]][i]
    return p

def Normalize(Probabilities):
    result = []
    suma = 1.5
    print(suma)
    for n in Probabilities:
        result.append(n/suma)
    return result

def Score(Motifs):
    k = len(Motifs[0])
    t = len(Motifs)
    cs = ConsensusWithPseudocounts(Motifs)
    score = 0
    for j in range(0,k):
        for i in range(0,t):
            if Motifs[i][j] != cs[j]:
                score += 1
    return score

def ConsensusWithPseudocounts(Motifs):
    k = len(Motifs[0])
    count = CountWithPseudocounts(Motifs)
    consensus = ""
    for j in range(k):
        m = 0
        frequentSymbol = ""
        for symbol in "ACGT":
            if count[symbol][j] > m:
                m = count[symbol][j]
                frequentSymbol = symbol
        consensus += frequentSymbol
    return consensus


