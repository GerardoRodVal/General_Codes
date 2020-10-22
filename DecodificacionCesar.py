from string import lowercase as abc
letras = list(abc)

palabra = 'gerarydoz'
pasos = 3

codificacion = []
for i in palabra:
    ind = letras.index(i)
    if( ind + pasos >= 25 ):
        nuevoInd = pasos - (26 - ind)
        i = letras[nuevoInd]
        codificacion.append(i)
    else:
        i = letras[ind+3]
        codificacion.append(i)

print palabra
print ''.join(codificacion)