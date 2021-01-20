from datetime import datetime, timedelta

def tiempo(hora):
    hora = hora.replace(' ', '')
    datetime_object = datetime.strptime(hora, '%H:%M:%S,%f')
    X = 2
    result = datetime_object + timedelta(seconds=X)
    result = ','.join(str(result.time()).split('.'))
    return result[:-3]

descargas = r'C:\Users\Gerar\Downloads'
entrada = open(descargas+'\D.A.R.Y.L.srt', encoding='utf8')
salida = open(descargas + '\sub_fix.srt', 'w+')
for row in entrada.readlines():
    row = row.strip().split('-->')
    try:
        final = row[1]
        final = tiempo(final)
        comienzo = row[0]
        comienzo = tiempo(comienzo)
        salida.write(str(comienzo) + ' --> ' + str(final) + '\n')
    except Exception as ex:
        salida.write(row[0] + '\n')
salida.close()

