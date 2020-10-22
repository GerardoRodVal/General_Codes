import argparse
from Bio import Entrez
import os
from Bio import SeqIO

print
Entrez.email = "g3rard095@hotmail.com"
parser = argparse.ArgumentParser(description='La entrada tiene que tener el formato parecido al siquiente: python archivo.py "especie" fastaAA.fasta porcIdntAA fastaND.fasta porcIdntND')
parser.add_argument('Especie', type=str, help='El nombre de la especie o genero que se quiere buscar, recomendado el uso de comillas DOBLES')       # comillas para evitar errores con espacio
parser.add_argument('filenameAA', type=argparse.FileType('r'),help='El archivo fasta de la secuencia de aminoacidos, extension .fasta')
parser.add_argument('PorcAA', type=int,help='Porcentaje de identidad que se asignara para secuencias de aminoacidos, un valor entero unico ')
parser.add_argument('filenameND', type=argparse.FileType('r'),help='El archivo fasta de la secuencia de nucleotidos, extension .fasta')
parser.add_argument('PorcND', type=int,help='Porcentaje de identidad que se asignara para secuencias de nucleotidos, un valor entero unico ')
args = parser.parse_args()
fasta1 = args.filenameAA
fasta2 = args.filenameND

Organismo = (args.Especie).lower()

handle = Entrez.espell(term=Organismo)                                          # Correcion taxonomica para el organismo de entrada
record = Entrez.read(handle)
E1 = record["Query"]                                                            # La entrada escrita
E2 = record["CorrectedQuery"]                                                   # la entrada correcta mas proxima
if( len(E2) == 0 ):                                                             # codigo para comparar correcion y original
    pass
else:
    print '[Error posible] Correcion taxonomica. Tal vez quisiste decir:', E2
    question = raw_input('Cambiar por entrada corregida? Y/N  ,N default ... ')
    if( question == 'y' or question == 'Y' ):                                   # Para cualquier que sea la entrada positiva
        E1 = E2
        print E1, ' ...Entrada cambiada con exito'
    else:                                                                       # si es cualquier otra cosa que no sea positivo, pasa
        print 'Entrada no cambiada'

# ------------------------------------------- Busqueda de secuencias en las bases de datos -----------------------------

handle = Entrez.esearch(db="nucleotide",term=E1)                                # base de datos de nucleotidos donde se busca
record = Entrez.read(handle)
Encontradas = record["Count"]                                                   # numero se secuencias encontradas
IDnd = record["IdList"]                                                         # identificadores de los organismos encontrados.\
print '\n'
print Encontradas,'secuencias encontradas en bases de datos de nucleotidos'

handle2 = Entrez.esearch(db="protein",term=E1)                                  # base de datos de proteinas donde se busca
record2 = Entrez.read(handle2)
Encontradas2 = record2["Count"]                                                 # numero se secuencias encontradas
IDaa = record2["IdList"]                                                        # identificadores de los organismo
print Encontradas2,'secuencias encontradas en bases de datos de proteinas'


# -------------------------------------------  Guardando dd la informacion  --------------------------------------------

Guardar = raw_input( "\n guardar esta informacion? ...  Y/N  ,N default: " )                    # Question para guardar archivo
if(  Guardar == 'Y' or Guardar == 'y' ):
    guardado = raw_input( '(sin extension) nombre del archivo ...  ')                      # libertad de elegir nombre
    archivo = open( guardado+'.txt', "w" )
    archivo.write('Entrada buscada: ' + Organismo+'\nEntrada corregida: ' + E1 +'\nNumero de secuencias enontradas de nucleotidos: ' + Encontradas +
                  '\nNumero de secuencias enontradas de proteinas: ' + Encontradas2)       # guardando la informacion en el archivo
    archivo.close()
    print 'Informacion guardada en el archivo '+guardado                                   # recepcion de decision
else:
    print 'Informacion no guardada'

# ------------------------------------------- Fasta de las secuencias encontradas --------------------------------------

Archivo2 = open('SecuenciasND.fasta',"w")                                                  # Guardando secuencais en fasta
print "\n Guardando todas las secuencias de la base de datos nucleotidica en archivo 'SecuenciasND.fasta'"
print "...Esto puede tardar dependiendo de la cantidad de secuencias..."
for i in IDnd:                                                                             # iterando en cada identificador de secuencia
    handle = Entrez.efetch(db="nucleotide", id=i, rettype="fasta", retmode="text", retmax=Encontradas)  # base de datos nucleotidica en cada identificados en el numero maximo de salidas.
    Archivo2.write( handle.read() )                                                        # guardando secuencias en el archivo creado
Archivo2.close()

print '\n \t \t Secuencias nucleotidicas guardadas con exito!'                             # slash ene -> salto de linea,   slash te -> tabulador(4 espacios)

Archivo3 = open('SecuenciasAA.fasta',"w")                                                  # Guardando secuencais en fasta
print "\n Guardando todas las secuencias de la base de datos de proteinas en archivo 'SecuenciasAA.fasta'"
print "...Esto puede tardar dependiendo de la cantidad de secuencias..."
for i in IDaa:                                                                             # iterando en cada identificador de secuencia de proteinas
    handle = Entrez.efetch(db="protein", id=i, rettype="fasta", retmode="text", retmax=Encontradas2)  # base de datos nucleotidica en cada identificados en el numero maximo de salidas.
    Archivo3.write( handle.read() )                                                        # guardando secuencias en el archivo creado
Archivo3.close()

print '\n \t \t Secuencias proteicas guardadas con exito!'


# ------------------------------------------- Alineamiento de secuencias -----------------------------------------------

question2 = raw_input('\n Desea alinear las secuencias de nucleotidos?...  Y/N  ,N default: ')          # question para alinear o no
if( question2 == 'Y' or question2 == 'y' ):
    os.system('muscle3.8.31_i86win32.exe -in SecuenciasND.fasta -out OutputND.fasta')                   # ejecuta linea de codigo en script en la consola
    print '\n \t Secuencias alineadas con exito!'
    print '\n \t Secuencias guardadas en archivo OutputND.fa \n'
else:
    print  'Las secuencias no se alinearan'

question3 = raw_input('\n Desea alinear las secuencias de proteinas?...  Y/N  ,N default: ')
if( question3 == 'Y' or question3 == 'y' ):
    os.system('muscle3.8.31_i86win32.exe -in SecuenciasAA.fasta -out OutputAA.fasta')
    print '\n \t Secuencias alineadas con exito!'
    print '\n \t Secuencias guardadas en archivo OutputAA.fa \n'
else:
    print  'Las secuencias no se alinearan \n'

# ------------------------------------------- Funcion adicional --------------------------------------------------------


# ------------------------------------------- Calculando identidad de Aminoacidos ---------------------------------------

identAA = []
secuenciasAA = []
for i in SeqIO.parse(fasta1, "fasta"):
    secuenciasAA.append(i.seq)
    identAA.append(i.description)

identND = []
secuenciasND = []
for i in SeqIO.parse("SecuenciasND.fasta", "fasta"):
    secuenciasND.append(i.seq)
    identND.append(i.description)

print 'Secuencias de nucleotidos parecidos en '+str(args.PorcAA)+'% a aminoacidos'
print '\t \t  \n Calculando... Espere.'

parecidas = []
parecidas2 = []
for i in range(len(identND)):
    for j in range(len(identAA)):
        a = open( "alineamiento.fasta", 'w' )
        try:
            a.write( '>'+identND[i] +'\n')
            a.write( str(secuenciasND[i]+'\n') )
            a.write( '>'+identAA[j]+'\n' )
            a.write( str(secuenciasAA[j]) )
            a.close()
            os.popen('muscle3.8.31_i86win32.exe -in alineamiento.fasta -out Salida.fasta')

            identif = []
            sec1 = []
            for k in SeqIO.parse("Salida.fasta", "fasta"):
                sec1.append(str(k.seq))
                identif.append(str(k.name)+str(k.id))
            cont = 0
            porc = 0
            for h in sec1:
                if( sec1[0][cont] == sec1[1][cont] ):
                    porc += 1
                cont += 1
            if( (porc*100)/len(sec1[0]) >= args.PorcAA ):
                parecidas.append( identif[0] )
                parecidas2.append( '>'+identif[0] )
                parecidas2.append(sec1[0]+'\n')
                print identif[0]
        except:
            pass
print '...'

Guardar2 = raw_input( "\n guardar esta informacion? ...  Y/N  ,N default: " )                    # Question para guardar archivo
if(  Guardar2 == 'Y' or Guardar2 == 'y' ):
    guardado = raw_input( '(sin extension) nombre del archivo ...  ')                      # libertad de elegir nombre
    archivo = open( guardado+'.txt', "w" )
    archivo.write("ID's y nombres de secuencias con porcentaje defino de coincidencia \n")    # guardando la informacion en el archivo
    for i in parecidas:
        archivo.write(i+'\n')                                                                   # guardando la informacion en el archivo
    archivo.close()
    print '\n \t \t Informacion guardada en el archivo '+guardado                                   # recepcion de decision
else:
    print '\n \t \t Informacion no guardada'

Guardar3 = raw_input( "\n guardar las secuncias en archivos fasta? ...  Y/N  ,N default: " )                    # Question para guardar archivo
if(  Guardar3 == 'Y' or Guardar3 == 'y' ):
    Archivo3 = open('IdentidadAA.fasta',"w")                                                  # Guardando secuencais en fasta
    print "\n Guardando todas las secuencias nucleotidicas con identidad en archivo 'IdentidadAA.fasta'"
    for i in parecidas2:
        Archivo3.write( i+'\n' )                                                        # guardando secuencias en el archivo creado
    Archivo3.close()
    print '\n \t \t Secuencias nucleotidicas guardadas con exito!'
else:
    print '\n \t \t Secuencias no guardadas'

# ------------------------------------------- Identidad de nucleotidos -------------------------------------------------

identND = []
secuenciasND = []
for i in SeqIO.parse(fasta2, "fasta"):
    secuenciasND.append(i.seq)
    identND.append(i.description)

identAA = []
secuenciasAA = []
for i in SeqIO.parse("SecuenciasAA.fasta", "fasta"):
    secuenciasAA.append(i.seq)
    identAA.append(i.description)

print 'Secuencias de nucleotidos parecidos en '+str(args.PorcND)+'% a aminoacidos'
print '\t \t  \n Calculando... Espere.'

parecidas = []
parecidas2 = []
for i in range(len(identAA)):
    for j in range(len(identND)):
        a = open( "alineamientoND.fasta", 'w' )
        try:
            a.write( '>'+identND[i] +'\n')
            a.write( str(secuenciasND[i]+'\n') )
            a.write( '>'+identAA[j]+'\n' )
            a.write( str(secuenciasAA[j]) )
            a.close()
            os.popen('muscle3.8.31_i86win32.exe -in alineamientoND.fasta -out SalidaND.fasta')

            identif = []
            sec1 = []
            for k in SeqIO.parse("SalidaND.fasta", "fasta"):
                sec1.append(str(k.seq))
                identif.append(str(k.name)+str(k.id))
            cont = 0
            porc = 0
            for h in sec1:
                if( sec1[0][cont] == sec1[1][cont] ):
                    porc += 1
                cont += 1
            if( (porc*100)/len(sec1[0]) >= args.PorcND ):
                parecidas.append( identif[0] )
                parecidas2.append( '>'+identif[0] )
                parecidas2.append(sec1[0]+'\n')
                print identif[0]
        except:
            pass
print '...'

Guardar5 = raw_input( "\n guardar esta informacion? ...  Y/N  ,N default: " )                    # Question para guardar archivo
if(  Guardar5 == 'Y' or Guardar5 == 'y' ):
    guardado = raw_input( '(sin extension) nombre del archivo ...  ')                      # libertad de elegir nombre
    archivo = open( guardado+'.txt', "w" )
    archivo.write("ID's y nombres de secuencias con porcentaje defino de coincidencia \n")    # guardando la informacion en el archivo
    for i in parecidas:
        archivo.write(i+'\n')                                                                   # guardando la informacion en el archivo
    archivo.close()
    print '\n \t \t Informacion guardada en el archivo '+guardado                                   # recepcion de decision
else:
    print '\n \t \t Informacion no guardada'

Guardar3 = raw_input( "\n guardar las secuncias en archivos fasta? ...  Y/N  ,N default: " )                    # Question para guardar archivo
if(  Guardar3 == 'Y' or Guardar3 == 'y' ):
    Archivo3 = open('IdentidadAA.fasta',"w")                                                  # Guardando secuencais en fasta
    print "\n Guardando todas las secuencias nucleotidicas con identidad en archivo 'IdentidadAA.fasta'"
    for i in parecidas2:
        Archivo3.write( i )                                                        # guardando secuencias en el archivo creado
    Archivo3.close()
    print '\n \t \t Secuencias nucleotidicas guardadas con exito!'
else:
    print '\n \t \t Secuencias no guardadas'





# Balaenidae
# Elephas maximus maximus
# Ailuropoda melanoleuca
