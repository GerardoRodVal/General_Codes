from datetime import datetime, timedelta


def tiempo(hora):
    hora = hora.replace(' ', '')
    datetime_object = datetime.strptime(hora, '%H:%M:%S,%f')
    X = -1
    result = datetime_object - timedelta(seconds=X)
    result = ','.join(str(result.time()).split('.'))
    return result[:-3]

entrada = open('D:\Videos\Pulse\Pulse.srt')
salida = open('D:\Videos\Pulse\Pulse2.srt', 'w+')
for row in entrada.readlines():
    row = row.strip().split('-->')
    try:
        final = row[1]
        final = tiempo(final)
        comienzo = row[0]
        comienzo = tiempo(comienzo)
        salida.write(str(comienzo) + ' --> ' + str(final) + '\n')
        print('escribiendo')
    except Exception as ex:
        print('escribiendo 2')
        salida.write(row[0] + '\n')
salida.close()