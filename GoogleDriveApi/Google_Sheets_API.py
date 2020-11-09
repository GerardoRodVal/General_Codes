from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import httplib2
import pandas as pd
import pickle
import os.path

class SHEETS:
    def credentials(self):
        Google_creds = 'service_account_file.json'
        Scopes = "https://www.googleapis.com/auth/drive, https://www.googleapis.com/auth/spreadsheets"
        credentials = service_account.Credentials.from_service_account_file(Google_creds, scopes=Scopes)
        return credentials

    def credentials2(self):
        '''Para cambiar las credenciales hay que eliminar el archivo toker.pickle y volver a ejecutar la funcion credentials'''
        SCOPES = ['https://www.googleapis.com/auth/drive',
                  "https://www.googleapis.com/auth/spreadsheets"]
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def move_docs(self, fileID, folderID):
        drive = build('drive', 'v3', credentials=self.credentials())
        # ------------------------------------ obten una lista de los archivos de mi drive -----------------------------
        #results = drive.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
        #items = results.get('files', [])
        # --------------------------------------------------------------------------------------------------------------

        file = drive.files().get(fileId=fileID).execute()
        try:
            #print(file.get('parents'))
            previous_parents = ",".join(file.get('parents'))
            drive.files().update(fileId=fileID,
                                 addParents=folderID,
                                 removeParents=previous_parents,
                                 fields='id, parents').execute()
            return 'Movido con exito!!'
        except:
            drive.files().update(fileId=fileID,
                                 addParents=folderID,
                                 removeParents='',
                                 fields='id').execute()
        return 'Movido con exito'

    def get_parents(self, folderID):
        '''Funcion para obtener el directorio (subcarpetas) a partir del ID de un forlder'''
        drive = build('drive', 'v3', credentials=self.credentials())
        folder = drive.files().get(fileId=folderID, fields='name, parents').execute()
        directorio = [folder['name']]
        while True:
            try:
                folder = drive.files().get(fileId=folder['parents'][0], fields='name, parents').execute()
                directorio.append(folder['name'])
            except:
                break
        directorio = '/'.join(directorio[::-1])
        return directorio

    def get_id(self, name, tipo='folder'):
        '''Obtener el ID de todos los folder o archivos (segun se especifique) a partir del nombre de entrada'''
        drive = build('drive', 'v3', credentials=self.credentials())
        results = []
        page_token = None
        if tipo == 'sheet':
            param = {'q': 'mimeType="application/vnd.google-apps.spreadsheet"'}
        else:
            param = {'q': 'mimeType="application/vnd.google-apps.folder"'}
        while True:
            try:
                if page_token:
                    param['pageToken'] = page_token
                files = drive.files().list(**param).execute()
                results.extend(files.get('files'))
                page_token = files.get('nextPageToken')
                if not page_token:
                    break
            except httplib2.HttpLib2Error as error:
                print(f'An error has occurred: {error}')
                break
        # el nombre de todos los archivos con su id
        #for i in results:
        #    print(i.get('name'), i.get('id'))

        try:
            IDs = [result.get('id') for result in results if result.get('name') in name]
        except Exception as e:
            IDs = None
            print(e)

        print(IDs)
        if len(IDs) >= 2:
            return IDs
        else:
            return IDs[0]

    # apartir de aqui. Funciones no probadas como funcionales
    def get_sheet(self, idsheet, header=1):
        drive = build('sheet', 'v2', credentials=self.credentials())
        sheets = drive.spreadsheets()
        result = sheets.values().get(spreadsheetId=idsheet).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            values = values[header - 1:]
            return values

    def get_sheet_df(self, name, pagerange='DATA', header=1):

        sheets = self.service.spreadsheets()
        idsheet = self.get_id(name)
        result = sheets.values().get(spreadsheetId=idsheet, range=pagerange).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            data = pd.DataFrame(values[1:], columns=values[header - 1])
            return data

