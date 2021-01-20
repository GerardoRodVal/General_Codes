from __future__ import print_function

import pandas as pd
import datetime
from GoogleDriveApi.Google_Sheets_API import SHEETS
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_foldersID():
    ruta = 'api/services/scheduler/'

    semanas = ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4']
    grados = ['K1', 'K2', 'K3', 'PF', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'M7', 'M8', 'M9']
    capsulas = ['Caligrafía', 'Gramática', 'Matemáticas', 'Ortografía']

    folders = SHEETS().get_id(semanas + grados + capsulas, 'folder')
    #folders = [SHEETS().get_id(i, 'folder') for i in semanas + grados + capsulas]                             # obteniendo los ids con el nombre de la lsita

    semanas_dir = {}                                                                                          # Formato: {ruta: ID}
    for id in folders:
        directorio = SHEETS().get_parents(id)                                                             # obteniendo el directorio del ID
        semanas_dir[directorio] = id

    rutas = {}
    for k in sorted(semanas_dir):                                                                             # Filtrando rutas
        if 'Recursos Knotion' in k:
            if 'Semana' in k.split('/')[-1]:
                rutas[k] = semanas_dir[k]
            elif 'Extra reto' in k.split('/')[1]:
                rutas[k] = semanas_dir[k]

    f = open(ruta + "rutas.txt", "w")
    f.write(str(rutas))
    f.close()

def recusos_move(df_log, dataframe, folderID):                                                                # funcion que itera sobre las ligas de recursos y mueve los documentos
    print(dataframe['Script / Link'])
    for link in dataframe['Script / Link'].fillna('0'):
        try:
            if link == '0':
                pass
            file = link.split('/')
            if file[2] == 'drive.google.com':
                fileID = file[-1].split('id=')[-1]
            else:
                fileID = file[-2]
            SHEETS().move_docs(fileID, folderID)                                                              # moviendo el archivo
            print('Recurso Movido con exito!!!')
        except:
            if link != '0':
                df_log.writelines(link + ',' + folderID + '\n')
                print('Error con folder ' + folderID)
                print('Error con archivo '+ link)
            continue

def recursos_dataframe(data, Pathway, Idioma, Grado, Capsula, sesion=False):                                # funcion que calcula los filtros para cada carpeta
    if sesion != False:
        dataframe = data[(data['Pathway'] == Pathway) &                                                       # selección de dataframe por sesion
                         (data['Idioma'] == Idioma) &
                         (data['Grado'] == Grado) &
                         (data['Capsula'] == Capsula) &
                         (data['Sesion'].between(sesion[0], sesion[1]))]
    else:
        dataframe = data[(data['Pathway'] == Pathway) &
                         (data['Idioma'] == Idioma) &
                         (data['Grado'] == Grado) &
                         (data['Capsula'] == Capsula)]
    return dataframe

def kinder(semanas_dir, df_log, data, reto):
    sesiones = [[1, 5], [6, 10], [11, 15], [16, 20]]
    grados_kinder = ['K1', 'K2', 'K3', 'PF']
    for grado in grados_kinder:
        for semana, sesion in enumerate(sesiones):
            # ----------------------------------------------------------------------------- KINDER ESPAÑOL
            directorio = 'Recursos Knotion /Kinder Español/Reto ' + reto + '/' + grado + '/Semana ' + str(semana + 1)
            kinder_espanol = recursos_dataframe(data, 'Español', 'ES', grado, 'Curricular', sesion)
            folderID = semanas_dir[directorio]
            recusos_move(df_log, kinder_espanol, folderID)
            print(directorio)
            # ------------------------------------------------------------------------------ KINDER INGLES
            directorio = 'Recursos Knotion /Kinder Inglés/Reto ' + reto + '/' + grado + '/Semana ' + str(semana + 1)
            kinder_ingles = recursos_dataframe(data, 'English', 'EN', grado, 'Curricular', sesion)
            folderID = semanas_dir[directorio]
            recusos_move(df_log, kinder_ingles, folderID)
            print(directorio)
    return 0

def primaria(semanas_dir, df_log, data, reto):
    curriculares = {'Formación Cívica y Ética': 'FOCE', 'Matemáticas': 'Matemáticas'}
    sesiones = [[1, 5], [6, 10], [11, 15], [16, 20]]
    grados_primaria = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6']
    for grado in grados_primaria:
        for semana, sesion in enumerate(sesiones):
            # --------------------------------------------------------------------------- PRIMARIA ESPAÑOL
            directorio = 'Recursos Knotion /Primaria Español/Reto ' + reto + '/' + grado + '/Semana ' + str(semana + 1)
            primaria_espanol = recursos_dataframe(data, 'Español', 'ES', grado, 'Curricular', sesion)
            folderID = semanas_dir[directorio]
            recusos_move(df_log, primaria_espanol, folderID)
            print(directorio)

            # ---------------------------------------------------------------------------- PRIMARIA INGLES
            directorio = 'Recursos Knotion /Primaria Inglés/Reto ' + reto + '/' + grado + '/Semana ' + str(semana + 1)
            primaria_ingles = recursos_dataframe(data, 'English', 'EN', grado, 'Curricular', sesion)
            folderID = semanas_dir[directorio]
            recusos_move(df_log, primaria_ingles, folderID)
            print(directorio)

        # --------------------------------------------------------------------- PRIMARIA CURRICULA ESPAÑOL
        for capsula in curriculares:
            if capsula == 'Matemáticas':
                for semana, sesion in enumerate(sesiones):
                    directorio = 'Recursos Knotion /Primaria Español/Reto ' + reto + '/' + grado + '/' + curriculares[
                        capsula] + '/Semana ' + str(semana + 1)
                    curricula_matematicas = data[(data['Pathway'] == 'Español') &
                                                 (data['Idioma'] == 'ES') &
                                                 (data['Grado'] == grado) &
                                                 (data['Capsula'] == 'Curricular') &
                                                 (data['Sesion'].between(sesion[0], sesion[1])) &
                                                 (data['Relacionado con...'] == 'Matemáticas')]
                    folderID = semanas_dir[directorio]
                    recusos_move(df_log, curricula_matematicas, folderID)
                    print(directorio)
            else:
                try:
                    directorio = 'Recursos Knotion /Primaria Español/Reto ' + reto + '/' + grado + '/' + curriculares[
                        capsula]
                    folderID = semanas_dir[directorio]
                    if capsula == 'Formación Cívica y Ética':
                        print(capsula)
                        curricula_espanol = recursos_dataframe(data, 'Formación Cívica y Ética', 'ES', grado, 'Curricular')
                        recusos_move(df_log, curricula_espanol, folderID)
                        print(directorio)
                    else:
                        curricula_espanol = recursos_dataframe(data, 'Español', 'ES', grado, capsula)
                        recusos_move(df_log, curricula_espanol, folderID)
                        print(directorio)
                except:
                    continue
    return 0

def secundaria(semanas_dir, df_log, data, reto):
    pathway_secundaria = {'Español': [[1, 5], [6, 10], [11, 15], [16, 20]],
                          'Matemáticas': [[1, 5], [6, 10], [11, 15], [16, 20]],
                          'Civics and Ethics': [[1, 2], [3, 14], [5, 6], [7, 8]],
                          'Chemistry': [[1, 6], [7, 12], [13, 18], [19, 24]],
                          'Geography': [[1, 4], [5, 8], [9, 12], [13, 26]],
                          'Global Citizenship': [[1, 5], [6, 10], [11, 15], [16, 20]],
                          'Historia': {'M7': [[1, 2], [3, 4], [5, 6], [7, 8]],
                                       'M8': [[1, 4], [5, 8], [9, 12], [13, 16]]},
                          'Physics': [[1, 6], [7, 12], [13, 18], [19, 24]],
                          'Biology': [[1, 4], [5, 8], [9, 12], [13, 16]],
                          'Tutoría': [[1, 1], [2, 2], [3, 3], [4, 4]],
                          'English Literacy': [[1, 5], [6, 10], [11, 15], [16, 20]]
                          }
    grados_secundaria = ['M7', 'M8', 'M9']
    folders = {'Español': 'Español', 'Matemáticas': 'Matemáticas', 'Civics and Ethics': 'FOCE',
               'Chemistry': 'Química', 'Geography': 'Geografía', 'Global Citizenship': 'Global',
               'Historia': 'Historia', 'Physics': 'Física', 'Biology': 'Biología', 'Tutoría': 'Tutoría',
               'English Literacy': 'English Literacy'}
    for grado in grados_secundaria:
        for path in pathway_secundaria:

            if grado == 'M7' and path == 'Historia':  # eligiendo sesiones
                sesiones = pathway_secundaria[path]['M7']
            elif (grado == 'M8' or grado == 'M9') and path == 'Historia':
                sesiones = pathway_secundaria[path]['M8']
            else:
                sesiones = pathway_secundaria[path]

            if path == 'English Literacy':
                idioma = 'EN'
            else:
                idioma = 'ES'

            for semana, sesion in enumerate(sesiones):
                try:
                    directorio = 'Recursos Knotion /Secundaria/Reto ' + reto + '/' + grado + '/' + folders[
                        path] + '/Semana ' + str(semana + 1)
                    secundaria = recursos_dataframe(data, path, idioma, grado, 'Curricular', sesion)
                    folderID = semanas_dir[directorio]
                    recusos_move(df_log, secundaria, folderID)
                    print(directorio)
                except:
                    continue
            curriculares = {'Destrezas Gramaticales': 'Gramática', 'Destrezas Ortográficas': 'Ortografía'}
            if path == 'Español':
                for capsula in curriculares:
                    directorio = 'Recursos Knotion /Secundaria/Reto ' + reto + '/' + grado + '/' + folders[path] + '/' + \
                                 curriculares[capsula]
                    secundaria_espanol = recursos_dataframe(data, 'Español', 'ES', grado, capsula)
                    folderID = semanas_dir[directorio]
                    recusos_move(df_log, secundaria_espanol, folderID)
                    print(directorio)
    return 0

def extra_reto(semanas_dir, df_log, data, reto):
    pathway_extra = {'Arte': ['Arte', 'K1', 'K2', 'K3', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'M7', 'M8', 'M9'],
                     'Educación Física': ['Educación Física', 'K1', 'K2', 'K3', 'PF', 'E1', 'E2', 'E3', 'E4', 'E5',
                                          'E6', 'M7', 'M8', 'M9'],
                     'Finance': ['Finanzas', 'K3', 'PF', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'M7', 'M8', 'M9'],
                     'Música': ['Música', 'K1', 'K2', 'K3', 'PF', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6'],
                     'Nutrition': ['Nutrición', 'K3', 'PF', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'M7', 'M8', 'M9'],
                     'OrganiK': ['OrganiK', 'K1', 'K2', 'K3', 'PF', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'M7', 'M8',
                                 'M9'],
                     'Technology': ['Tecnología', 'K1', 'K2', 'K3', 'PF', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'M7',
                                    'M8', 'M9'],
                     'Heedfulness': ['Heedfulness', 'K1', 'K2', 'K3', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'M7', 'M8',
                                     'M9']
                     }

    for path in pathway_extra:
        for grado in pathway_extra[path][1:]:

            if path == 'Finance' or path == 'OrganiK':
                idioma = 'EN'
            else:
                idioma = 'ES'

            capsula = 'Curricular'
            if path == 'Finance' or path == 'Nutrition' or path == 'OrganiK' or path == 'Heedfulness':
                capsula = pathway_extra[path][0]
            if path == 'Arte' and grado in ['K1', 'K2', 'K3']:
                capsula = 'Expresión Artística'

            directorio = 'Recursos Knotion /Extra reto/Reto ' + reto + '/' + pathway_extra[path][0] + '/' + grado
            extra = data[(data['Pathway'] == path) &
                         (data['Idioma'] == idioma) &
                         (data['Grado'] == grado) &
                         (data['Capsula'] == capsula)]
            folderID = semanas_dir[directorio]
            recusos_move(df_log, extra, folderID)
            print(directorio)
    return 0

def recursos_main():
    print('Iniciando recursos!!!')

    for reto in ['4']:
        data = pd.read_csv('reto_'+reto+'.csv')
        df_log = open("ligas_drive_"+reto+".txt", "w")
        semanas_dir = eval(open("rutas.txt", 'r', encoding="utf8").read())

        #kinder(semanas_dir, df_log, data, reto)
        primaria(semanas_dir, df_log, data, reto)
        secundaria(semanas_dir, df_log, data, reto)
        extra_reto(semanas_dir, df_log, data, reto)

        df_log.close()
        print('Recursos terminados!!!')

recursos_main()
#folderID = '1SWnnc6DEjuwGbwem-3sO8GEN_2Gz_e4x'
#fileID = '1Gqe1dVL7VWP_ZKbR9B5cvx6BI6PhV_4_TZm7WVPks-Q'
#SHEETS().move_docs(fileID, folderID)
