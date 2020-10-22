from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import httplib2
import pandas as pd

class SHEETS:

    def credentials(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def move_docs(self, fileID, folderID):
        service = build('drive', 'v3', credentials=self.credentials())
        service.files().update(fileId=fileID,
                               addParents=folderID,
                               removeParents='',
                               fields='id, parents').execute()
        '''

        drive = build('drive', 'v3', credentials=self.credentials())
        print(drive)
        file = drive.files().get(fileId=fileID, fields='parents').execute()
        try:
            previous_parents = ",".join(file.get('parents'))
            file = drive.files().update(fileId=fileID,
                                        addParents=folderID,
                                        removeParents=previous_parents,
                                        fields='id, parents').execute()
            return 'Movido con exito!!'
        except:
            file = drive.files().update(fileId=fileID,
                                        addParents=folderID,
                                        removeParents='',
                                        fields='id, parents').execute()
            return 'Movido con exito'
    '''
    '''
    def get_sheet(self, idsheet, pagerange, header=1):
        sheets = self.service.spreadsheets()
        result = sheets.values().get(spreadsheetId=idsheet, range=pagerange).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            values = values[header - 1:]
            return values

    def get_sheet_df(self, name, pagerange='DATA', header=1):
        """
        SAMPLE_spreadsheetId= '1kRJG8h9msa8ld0CZBDM2TxEn4nNc5KQChYMqW1pCViA'
        SAMPLE_pagerange = 'ISCO4!A2:E'
        """
        sheets = self.service.spreadsheets()
        idsheet = self.get_id(name)
        result = sheets.values().get(spreadsheetId=idsheet, range=pagerange).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            data = pd.DataFrame(values[1:], columns=values[header - 1])
            return data

    def get_parents(self, folderID):
        folder = self.drive.files().get(fileId=folderID, fields='name, parents').execute()
        directorio = [folder['name']]
        while True:
            try:
                folder = self.drive.files().get(fileId=folder['parents'][0], fields='name, parents').execute()
                directorio.append(folder['name'])
            except:
                break
        directorio = '/'.join(directorio[::-1])
        return directorio

    

    def get_id(self, name, tipo='sheet'):
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

                files = self.drive.files().list(**param).execute()
                results.extend(files.get('files'))
                page_token = files.get('nextPageToken')
                if not page_token:
                    break
            except httplib2.HttpLib2Error as error:
                print(f'An error has occurred: {error}')
                break
        try:
            IDs = [result.get('id') for result in results if result.get('name') in name]
        except Exception as e:
            IDs = None
            print(e)

        if len(IDs) >= 2:
            return IDs
        else:
            return IDs[0]
    '''