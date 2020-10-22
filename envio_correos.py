# encode utf-8

from math import sin, cos, sqrt, asin, pi
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
import ast

file = pd.read_csv("utils/comercialKnn/data/tidy/Escuelas_para_publicitar.csv")
file = file.drop( ['Unnamed: 0', 'Unnamed: 0.1', 'index'], axis=1 )                                           # Eliimnando columnas


def Haversine( lat1, lon1, lat2, lon2 ):

    r = 6371000                                                                                               # Radio terrestre en metros
    c = pi/180
    d = 2*r*asin(sqrt(sin((c*(lat2-lat1)/2)**2) + cos(c*lat1)*cos(c*lat2)*sin((c*(lon2-lon1))/2)**2))         # Ecuacion de Haversine
    return d/1000


lat_knotion = 19.696065                                                                                       # Coordenadas de knotion
lon_knotion = -101.113509
distancias = []
for coor in file['coordenadas']:
    try:
        coor = dict(ast.literal_eval(coor))
        lat = coor['lat']
        lon = coor['lng']
        distancias.append(Haversine(lat, lon, lat_knotion, lon_knotion))
    except:
        distancias.append('N/A')
        pass
file['Distancia a knotion (km)'] = distancias                                                                 # Agregando distancias en kilometros


def Email( email_data ):

    username = 'gerardo.rodriguez@knotion.com'                                                                # Usuario del correo donde se enviaran
    password = 'pass'                                                                                         # contasena del correo que enviara
    for indice in range(len(email_data)):
        fromaddr = 'gerardo.rodriguez@knotion.com'                                                            # Correo remitente
        #toaddrs = email_data['Correo electrónico'].iloc[indice]                                                # Indice de cada correo en el dataframe
        toaddrs = 'g3rard095@hotmail.com'                                                                     # Correo destinatario
        asunto = "Este es un asunto"
        msg = 'Correo enviado utilizando Python'
        mensaje = 'Subject: {}\n\n{}'.format(asunto, msg)

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)                                                                      # iniciando sesion
        if toaddrs != 0.0 or toaddrs != 'N/A':                                                                # Para los correos que esten registrados
            server.sendmail(fromaddr, toaddrs, mensaje)                                                       # Envia el correo
            print('Correo enviado a %s' % toaddrs)                                                            # Mensaje de salida
        else:
            print('No se pudo enviar el correo\n\tDestinatario invalido ... %s \n' % toaddrs)                 # Mensaje de salida de no enviado
        server.quit()
    return 0


#Email(file)