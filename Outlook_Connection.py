def EmailExtraction(folder):
    today = date.today()
    print("Today's date:", today)
    Mensajes = folder.Items
    # CHECAR EL ORDEN DE LOS CORREOS ARROJADOS
    for i, mail in enumerate(Mensajes):
        #print(mail.Unread)
        if i == 10:
            break
        else:
            nombre = mail.SenderName
            correo = mail.SenderEmailAddress
            cuerpo = mail.Body
            asunto = mail.Subject
            adjunto = mail.Attachments
            print('------------------------------------------')


def Authentication():
    global outlook
    global account

    outlook = win32com.client.Dispatch("outlook.application").GetNamespace("MAPI")

    cuenta = outlook.Folders.Item(1)
    for folder in cuenta.Folders:
        if str(folder.Name) == 'Bandeja de entrada':
            EmailExtraction(folder)