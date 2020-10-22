from bioservices.uniprot import UniProt
from Bio import Entrez
import xml.etree.ElementTree as ET

Entrez.email = "g3rard095@hotmail.com"

def Correcion(Especie):
    handle = Entrez.espell(term=Especie.lower())  # Correcion taxonomica para el organismo de entrada
    record = Entrez.read(handle)
    E1 = record["Query"]  # La entrada escrita
    E2 = record["CorrectedQuery"]  # la entrada correcta mas proxima
    if (len(E2) == 0):  # codigo para comparar correcion y original
        pass
    else:
        print ('\n \n[Error posible] Correcion taxonomica. Tal vez quisiste decir:', E2)
        question = input('Cambiar por entrada corregida? Y/N  ,N default ... ')
        if (question == 'y' or question == 'Y'):  # Para cualquier que sea la entrada positiva
            E1 = E2
            print (E1, '\n \t ...Entrada cambiada con exito')
        else:  # si es cualquier otra cosa que no sea positivo, pasa
            print ('\n \t Entrada no cambiada')
    return E1

def Fasta(Especie):
    Proteinas = open( "Ex3Proteinas.fasta",'w' )                                                        # creando archivo para las proteinas encontradas
    Proteinas.write(UniProt().search(Especie, frmt="fasta"))                                            # Accediendo a uniprot en formato fasta
    print('\n \t Proteinas encontradas guardadas exitosamente en archivo "Ex3Proteinas.fasta" \n')      # mensaje de salida
    return Proteinas.close()

def Alternos(Especie):
    NombresAlt = open( "Ex3Alternos.txt",'w' )                                                          # Archivo para los nombres alternos
    nombres = (UniProt().search(Especie, frmt="tab", columns='id,protein names').split('\n'))           # Accediendo a uniprot en formato tab, solo columnas especificas
    NombresAlt.write('\t\t\t\tNOMBRES ALTERNOS DE PROTEINAS\n')                                         # Titulo
    for i in nombres[1:]:                                                                               # iterando en cada nombre
        nombre = (i.split('('))                                                                         # Separando los nombres alternos
        try:
            NombresAlt.write( 'Nombre de la proteina \n'+'\t'+nombre[0] )                               # Agregando el nombre base de la proteina
            NombresAlt.write('\n\t--Nombres alternos de la proteina \n')
            for j in nombre[1:]:                                                                        # iterando sobre cada nombre alterno
                NombresAlt.write('\t\t\t('+j+'\n')                                                      # Agregando cada nombre alterno
            NombresAlt.write('\n\n')
        except:
            continue
    print('\n \t Nombres alternos guardados exitosamente en archivo "Ex3Alternos.txt" \n')            # mensaje de salida
    return NombresAlt.close()

def Anotaciones(Especie):
    Anot = open( "Ex3Anotaciones.gff",'w' )
    Anot.write(UniProt().search(Especie, frmt="gff"))
    print('\n \t Anotaciones guardadas exitosamente en archivo "Ex3Anotaciones.gff" \n')            # mensaje de salida
    return Anot.close()

def Estructuras(Especie):
    Estruc = open("Ex3Estructuras.xml", 'w')
    archivo = UniProt().search(Especie, frmt="xml")
    root = ET.fromstring(archivo)
    for child in root:
        for child2 in child:
            if (child2.tag[28:]=='name'):
                Estruc.write('Nombre de la proteina \n')
                Estruc.write('  '+str(child2.text)+'\n')
                Estruc.write('\t Estructura secundaria y terciaria de la proteina \n')
            if(child2.tag[28:] == 'feature'):
                if (str(child2.attrib)[10:23]=='transmembrane'):
                    Estruc.write('\t'+'  '+str(child2.attrib)+'\n')
            if (child2.tag[28:] == 'evidence'):
                    Estruc.write('\t' + '  ' + str(child2.attrib) + '\n')
            else:
                continue
    print('\n \t Estructuras guardadas exitosamente en archivo "Ex3Estructuras.xml" \n')            # mensaje de salida
    return Estruc.close()

def proteinas( Especie ):
    Especie = Correcion(Especie)
    print( '\n 1. Lista de proteinas \n 2. Nombre alterno de proteinas \n 3. Anotacioness \n 4. Estructuras secundaria y terciaria \n' )
    busqueda = list(map(int,(input("Cual de las siguientes busquedas desea hacer? (elija un numero o varios separados por comas): " ).split(','))))
    for i in busqueda:
        try:
            if( i == 1 ):
                Fasta(Especie)
            if( i == 2 ):
                Alternos(Especie)
            if (i == 3):
                Anotaciones(Especie)
            if (i == 4):
                Estructuras(Especie)
        except:
            continue


proteinas( input('\n Ingresa en nombre de la especie: ') )


# Balaenidae, P43403