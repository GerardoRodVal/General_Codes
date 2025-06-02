from datetime import datetime, timedelta

print('\n'+'*'*100)
print('\n Este programa sincroniza los subtitulos, adelantandolos o atrasandolos para que coincidan con el audio \n')

path = input('ruta del archivo de subtitulos:')
print('archivo cargado...')

extra_time = input('tiempo de diferencia:')
try: file = open(path, encoding='latin1')
except Exception as E: print('Error:', E)

out_name = path.split('\\')[-1]
new_file = open(out_name, encoding='utf8', mode='w+')

def add_time(time, extra_time):
    row_time, row_ms = time.split(',')
    row_time = datetime.strptime(row_time, '%H:%M:%S')
    new_time = row_time + timedelta(seconds=float(extra_time))

    row = str(new_time.time()) + ',' +(row_ms)
    return row

fix_sub = []
for row in file.readlines():
    if '-->' in row:
        init, fin = row.split(' --> ')
        init = add_time(init, extra_time)
        fin = add_time(fin, extra_time)
        row = init + ' --> ' + fin
    new_file.write(str(row))
    #fix_sub.append(row)
#new_sub = ''.join(fix_sub)
new_file.close()

print('\n'+'*'*100)


