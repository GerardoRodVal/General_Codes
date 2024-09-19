from datetime import datetime, timedelta
import os
import keyboard
from unicodedata import numeric

class subtitles_config:
    def __init__(self):
        self.path_out = r'C:\Users\gerardo_offline\Desktop\\'
        print('Búsqueda por default: > C:\\Users\\gerardo_offline\\')
        print('> modificar ruta (y/n)...')
        self.sub_path = r'C:\Users\gerardo_offline'
        while True:
            if keyboard.is_pressed('y'):
                self.sub_path = input('ruta de los subtitulos:') + '\\'
                break
            elif keyboard.read_event().event_type == 'down': break

    def choose_file(self):
        print('> buscando archivos...\n')
        files = list(os.walk(self.sub_path))
        i = 0
        files_dir = {}
        for dirpath, dirnames, filenames in os.walk(self.sub_path):
            for file_i in filenames:
                name, ext = os.path.splitext(file_i)
                if ext != '.srt': continue
                print('{0} - {1}'.format(i,file_i))
                files_dir[i] = dirpath+'\\'+file_i
                i += 1
        print('\n Elige el número del archivo a modificar... \n')
        stop = False
        while stop == False:
            file_i = input('> ')
            try:
                file_i = int(file_i)        # si es un número
                if file_i > len(files)-1: raise ValueError
                stop = True
            except:
                print('...valor incorrecto')
                continue
        file_name = files_dir[file_i]
        return file_name

    def operate_time(self, time_f, dif):
        dif = dif.split('.')
        if len(dif) > 1: dec = int(dif[1])
        else: dec = 0
        ent = int(dif[0])

        time_f = time_f.replace(' ', '')
        time_f = datetime.strptime(time_f, '%H:%M:%S,%f')
        time_f = time_f + timedelta(seconds=ent, microseconds=dec*1000)
        time_f = ','.join(str(time_f.time()).split('.'))
        time_f = time_f[:-3]

        return time_f

    def read_file(self, file):
        print('\n Diferencia de tiempo en segundos (+/-)')
        print('para sumas mas precisas agregar punto decimal\n')
        dif = input('> ')

        filename = file.split('\\')[-1]
        for encode_f in ['utf8', 'latin1']:
            file_input = open(file, 'r', encoding=encode_f)
        out_file = open(self.path_out + filename, 'w+')
        for row in file_input.readlines():
            row = row.strip().split('-->')
            if len(row) == 2:
                t_ini = self.operate_time(row[0], dif)
                t_fin = self.operate_time(row[1], dif)
                out_file.write(str(t_ini) + ' --> ' + str(t_fin) + '\n')
            else:
                out_file.write(row[0] + '\n')
        out_file.close()
        print('...Terminado')

sub_config = subtitles_config()
archivo = sub_config.choose_file()
sub_config.read_file(archivo)
