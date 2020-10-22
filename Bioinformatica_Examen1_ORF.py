from Bio.Seq import Seq                 # modelo para el complemento de la secuncia
import Bio.Data.CodonTable as codones
import textwrap as tw                   # Modulo para separar el texto

Co_Am = \
   {"TTT":"Phe", "TTC":"Phe", "TTA":"Leu", "TTG":"Leu",
    "TCT":"Ser", "TCC":"Ser", "TCA":"Ser", "TCG":"Ser",
    "TAT":"Tyr", "TAC":"Tyr", "TAA":"STOP", "TAG":"STOP",
    "TGT":"Cys", "TGC":"Cys", "TGA":"STOP", "TGG":"Trp",
    "CTT":"Leu", "CTC":"Leu", "CTA":"Leu", "CTG":"Leu",
    "CCT":"Pro", "CCC":"Pro", "CCA":"Pro", "CCG":"Pro",
    "CAT":"His", "CAC":"His", "CAA":"Gln", "CAG":"Gln",
    "CGT":"Arg", "CGC":"Arg", "CGA":"Arg", "CGG":"Arg",
    "ATT":"IIe", "ATC":"IIe", "ATA":"IIe", "ATG":"Met",
    "ACT":"Thr", "ACC":"Thr", "ACA":"Thr", "ACG":"Thr",
    "AAT":"Asn", "AAC":"Asn", "AAA":"Lys", "AAG":"Lys",
    "AGT":"Ser", "AGC":"Ser", "AGA":"Arg", "AGG":"Arg",
    "GTT":"Val", "GTC":"Val", "GTA":"Val", "GTG":"Val",
    "GCT":"Ala", "GCC":"Ala", "GCA":"Ala", "GCG":"Ala",
    "GAT":"Asp", "GAC":"Asp", "GAA":"Glu", "GAG":"Glu",
    "GGT":"Gly", "GGC":"Gly", "GGA":"Gly", "GGG":"Gly",}

def Complemento( secuencia ):
    secuencia = list(secuencia)
    for i in range(len(secuencia)):
        if( secuencia[i] == 'C' ):
            secuencia.pop(i)
            secuencia.insert(i,'G')
        elif (secuencia[i] == 'A'):
            secuencia.pop(i)
            secuencia.insert(i, 'T')
        elif (secuencia[i] == 'G'):
            secuencia.pop(i)
            secuencia.insert(i, 'C')
        elif (secuencia[i] == 'T'):
            secuencia.pop(i)
            secuencia.insert(i, 'A')
    return ''.join(secuencia)

def SeisMarcos( secuencia, secuenciaC ):
    cont = 0                                                                # definiendo marcos de lectura cada 3 caracteres
    cont2 = 3
    cont3 = 0
    cont4 = 3
    M1,M2,M3,m1,m2,m3 = [], [], [], [], [], []

    for i in range(len(secuencia)/3):                                       # Creando marcos de lectura para secuencia normal
        try:
            M1.append( secuencia[cont:cont2] )                              # marco de lectura normal sin alteraciones
            M2.append(('  '+secuencia)[cont:cont2] )                        # marco de lectura +2 con un espacio a la derecha
            M3.append((' ' + secuencia)[cont:cont2])                        # marco de lectura +3 con dos espacios a la derecha
            m1.append(secuenciaC[cont3:cont4])
            m2.append((' ' + secuenciaC[::-1])[cont3:cont4])
            m3.append(('  ' + secuenciaC[::-1])[cont3:cont4])
            cont += 3
            cont2 += 3
            cont3 += 3
            cont4 += 3
        except:
            continue

    return M3,M2,M1,m1,m2,m3

def MarcoL( Entrada ):                                                      # remplazar la E mayuscula para el formato original
    entrada = []                                                            # anexados para leer secuencia en archivo
    for i in Entrada:
        entrada.append(i.strip())
    entrada =''.join(entrada)                                               # termina anexo
    a = list(set(entrada))

    if( a == ['A','C','T','G'] ):
        secuencia = str(Seq( entrada ))                                          # creando la entrada como secuencia y convirtiendola en String
        secuenciac = str(Seq( entrada ).complement())                            # Complemento de la secuencia
        #secuenciaC = Complemento( secuencia )

        #ML = list(SeisMarcos( secuencia,secuenciac ))                            # creando los 6 marcos de lectura


        M3 = tw.wrap(' ' + secuencia,3)                                         # Definiendo los 6 marcos de lectura
        M2 = tw.wrap('  ' + secuencia,3)
        M1 = tw.wrap(secuencia,3)
        m1 = tw.wrap(secuenciac[::-1],3)
        m2 = tw.wrap(' ' + secuenciac[::-1],3)
        m3 = tw.wrap('  ' + secuenciac[::-1],3)
        ML = [M3,M2,M1,m1,m2,m3]

        cont = 3

        for Marcos in ML:                                                        # Analizando cada marco de lectura
            if( cont == 0 ):                                                     # if solo para que sea vea bonito
                cont -= 1
            print "\n --Marco de lectura", str(cont)
            print '  ',Marcos
            orfs = []
            indices = []                                                         # lista indices de codones iniciales
            contador = 0                                                         # contador de codones (para longitudes de orfs)
            for codon in Marcos:                                                 # Analizando los codones de cada marco de lectura
                contador += 1                                                    # aumentando contador por codon
                if( codon == 'ATG' ):                                            # Buscando codon inicial.
                    indices.append( contador )
                elif( codon == 'TAA' or codon == 'TAG' or codon == 'TGA' ):      # Buscando codones finales.
                    try:
                        for inicios in indices:                                  # buscando todos los orfs anidados
                            distanciaT = ((contador - inicios) + 1)
                            orfs.append( (distanciaT, inicios) )                 # Restando valor de contador desde codon In hasta el Fin para calcular longitud
                        indices = []                                             # limpiando la lista despues de codon de termino
                    except:
                        pass                                                     # pass, "ignora", pasalo por alto

            print "--Cantidad de ORF en marco de lectura: ", len(orfs)
            if(len(orfs) == 0):
                orfs.append( 'sin marcos de lectura' )
                print orfs
            else:
                O_m = sorted(orfs)[-1]                                                                          # Ordenand ORF, menor a mayor segun distancia
                mayor = Marcos[O_m[1] - 1:(O_m[0] + O_m[1]) - 1]
                print "--ORF mayor dentro del marco de lectura con longitud de "+str(O_m[0])+" codones"
                print '  ', ''.join(mayor)                                                                               # Orf mayor calculado del indice del ATG, hasta la suma del indice mas la distancia)
                print "--Secuencia de Aminoacido del orf"
                Aminoacidos = []                                                                                # Lista de aminoacidos
                for i in mayor:
                    Aminoacidos.append( Co_Am[i] )                                                              # para cada codon del orf mas grande
                print '  ', Aminoacidos
            cont -= 1
        return codones.standard_dna_table                                                    # Tabla para que se vea bonito :)
    else:
        return 'No es una secuencia de ADN'

print MarcoL( open("C:\Users\G3rar\Desktop\Archivos\entrada.txt", 'r') )                          # Anexado para leer con archivo
#print MarcoL( raw_input('Ingresa secuencia:   ').upper().strip() )                               # Imprimiendo tablas de codones con respectivos AA's




# ACGTTGTAGCTACGTACGATCTAGCTAGCTAGCTAGTGCATCGATGCATCGATGCA
# AGCTATTAAAAGAGGAAATCCACAATAATCGGAAATAGAAAGACAAGTTTGGTTAGCGGAACGTTTCAACGCCATTTTTCCCGGCCAAAGCTAACTCTAACTAACTCTTTGTTTTTTTTCGGTTTTTGTGCCATCTTCCAGTTTTCATTTTTTTTGTTTCCCCTCTATCTTTTTGGGTAATAGGGTTTCTAATCTCTGGGACAAACTCCAATCGTTTCGAATCCGCAATGCCCAGATGGTCGATCAATAGAAATATCAAGAGTCTCCAATTCCAAAGGCTAAATCTTTGAGATCTTTTTTTTTATAAATTTCCCTGAAATTAATAAACTTTGAGGGGAAATGAGCGCTTCGAGGTTCGTAAAGTGCGTGACGGTTGGTGATGGAGCTGTCGGAAAAACTTGTTTGTTGATTTCTTACACAAGCAACACTTTCCCTACGGTTATGTCCCAATTATTCTTTCATGTTTCTTGTTTCATTACCACAACAACAACATATCTCATGTTTCTTGTTTCTTTTGTGGATATACAGGATTATGTGCCTACCGTTTTCGATAATTTCAGTGCCAATGTTGTGGTTAATGGAAGCACTGTGAATCTTGGATTGTGGGACACTGCAGGTTTTTCATTTTCCTATATATCTTGGTGTTTGAAATTTGGAATATGGTTTTTGGATCTGAAGATTTTGAAAATTTGGGTATGAATAAACAGGGCAAGAGGATTACAATAGATTAAGACCACTGAGTTACCGTGGAGCAGATGTTTTCATTTTGGCCTTCTCTCTTATCAGTAAAGCCAGTTATGAAAACGTCTCCAAAAAGGTTTTAAAAATCCATCAATCTTGTTTCATATTATTGAGTTTTCGTCACATTTTTTGAACTCTTGTCACAAATTGTGTTTGCAGTGGATCCCGGAGTTGAAACATTACGCGCCTGGTGTCCCCATCGTCCTTGTTGGAACAAAGCTTGGTGAGTTTTCCATTGTTTTTTCCTGATCTCGCTCCTTTTACTTTATTAGTTGTGACTGATGTGTTTTTGCTCTCCAGATCTTCGAGATGATAAACAGTTCTTTATCGACCATCCTGGTGCTGTTCCGATTACTACTGCTCAGGGAGAGGAGCTGAGGAAGCAAATAGGAGCACCTACTTACATCGAATGCAGTTCCAAAACTCAAGAGGTACGTAGATTAGTATATATACCCTTGTTGCAGATTTCTAATGTTAATGTTAATGCTAATGTTGATGATGTGAGAGTGCAGAATGTGAAGGCGGTGTTTGACGCAGCCATCCGAGTGGTGTTGCAACCGCCAAAGCAGAAGAAGAAGAAGAGCAAAGCGCAGAAGGCATGCTCCATTCTATGATGATTGGAAATCTCTGTTTTTATGTATTTGGTTTTGGTATATTAATCTTCTAACAATGAATGAATCAATGTGTTAATGGACAGACACCCAAGTTTGACTGGTCCTTTTTGTTCTTAATATTAATGGAGTTTGTCGGAATCAACGTTTCTTTTGCTTCTACGATTCAGTCCTATGCATA
