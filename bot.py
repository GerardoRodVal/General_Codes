import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import datetime as dt
import time

def get_dia_code(dia, driver):

    dia_format = 'body > div.ng-trigger.ng-trigger-overlayAnimation.ng-tns-c61-22.p-datepicker.p-component.' \
                 'p-datepicker-touch-ui.ng-star-inserted > div.p-datepicker-group-container.ng-tns-c61-22.' \
                 'ng-star-inserted > div > div.p-datepicker-calendar-container.ng-tns-c61-22.' \
                 'ng-star-inserted > table > tbody > tr:nth-child({}) > td:nth-child({})'

    att_descrp = dia_format.format('0','0')

    inicio_mes = False
    fin_mes = False
    print('dia_actual', dia)
    for fila in range(1,6):

        for columna in range(1,8):
            dia_actual = dia_format.format(str(fila), str(columna))
            att_descrp = driver.find_elements(By.CSS_SELECTOR, dia_actual)[0].get_attribute("innerHTML")                # descripcion del atributo

            print('att_descrp', att_descrp)
            stop = 0
            while stop != -1:

                ini = att_descrp.find('<')
                fin = att_descrp.find('>')
                stop = ini
                if stop == -1: break
                att_descrp = att_descrp[:ini] + att_descrp[fin+1:]

            if inicio_mes and int(att_descrp) == 1: fin_mes = True                                              # el segundo 1 marca otro mes
            if int(att_descrp) == 1: inicio_mes = True                                                          # el primer 1 marca el inicio de mes

            if fin_mes and inicio_mes: continue
            if inicio_mes == False: continue
            print('att_descrp final', att_descrp)
            print(dia, att_descrp)
            print(int(dia) == int(att_descrp))
            print(dia_actual)
            print('-'*100)
            if int(dia) == int(att_descrp):
                return dia_actual

def Main_bot():

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")

    browser = webdriver.Chrome(executable_path='.\\selenium_chrome\\chromedriver.exe', chrome_options=chrome_options)
    browser.maximize_window()
    browser.get('https://cts-appp.herokuapp.com/#/login')

    weekend = ['Saturday','Sunday']
    today = dt.datetime.today()
    semana_habil = [(today+dt.timedelta(i)).day for i in range(7) if (today+dt.timedelta(i)).strftime("%A") not in weekend]   # guarda los dias que no sean fines de semana

    # ----------------------------------------------------------------------- LOGIN
    user = 'body > cts-root > cts-login > div > div > form > input'
    driver = browser.find_elements(By.CSS_SELECTOR, user)[0]
    driver.send_keys('gerardo.rodriguezv@ab-inbev.com')

    pass_ = 'body > cts-root > cts-login > div > div > form > p-password > div > input'
    driver = browser.find_elements(By.CSS_SELECTOR, pass_)[0]
    driver.send_keys('Cerveza.inbev!')

    boton_login = 'body > cts-root > cts-login > div > div > form > button'
    browser.find_elements(By.CSS_SELECTOR, boton_login)[0].click()

    time.sleep(3)

    # ----------------------------------------------------------------------- APARTANDO LUGAR
    reservar_boton = 'body > cts-root > cts-main > div > div.layout-main > div > div > div > div > div > div > div:nth-child(3) > button'
    browser.find_elements(By.CSS_SELECTOR, reservar_boton)[0].click()
    time.sleep(1)

    # apartar mediante el calendario
    calendario_opcion = 'body > cts-root > cts-main > div > div.layout-main > div > div > div > div > div > div > div:nth-child(3) > p-menu > div > ul > li:nth-child(1)'
    browser.find_elements(By.CSS_SELECTOR, calendario_opcion)[0].click()
    time.sleep(3)

    # click boton de apartar dia
    apartar_dia_boton = 'body > cts-root > cts-main > div > div.layout-main > div > cts-calendar > div > div > div > div > div:nth-child(1) > button:nth-child(1)'
    browser.find_elements(By.CSS_SELECTOR, apartar_dia_boton)[0].click()
    time.sleep(1)

    for dia in semana_habil:

        calendario_dias = 'body > cts-root > cts-main > div > div.layout-main > div > cts-calendar > p-dialog.p-element.custom-dialog.ng-tns-c34-15.ng-star-inserted > div > div > div.ng-tns-c34-15.p-dialog-content > form > div:nth-child(1) > p-calendar > span > button'
        browser.find_elements(By.CSS_SELECTOR, calendario_dias)[0].click()
        time.sleep(1)

        # ********************************************************************
        next_month = 'body > div.ng-trigger.ng-trigger-overlayAnimation.ng-tns-c61-22.p-datepicker.p-component.p-datepicker-touch-ui.ng-star-inserted > div.p-datepicker-group-container.ng-tns-c61-22.ng-star-inserted > div > div.p-datepicker-header.ng-tns-c61-22 > button.p-ripple.p-element.p-datepicker-next.p-link.ng-tns-c61-22'
        browser.find_elements(By.CSS_SELECTOR, next_month)[0].click()
        time.sleep(1)
        # ********************************************************************

        dia_obj_format = get_dia_code(dia, browser)
        print('ReSULTADO', dia_obj_format)
        return 0
        #dia_actual = 'body > div.ng-trigger.ng-trigger-overlayAnimation.ng-tns-c61-22.p-datepicker.p-component.p-datepicker-touch-ui.ng-star-inserted > div.p-datepicker-group-container.ng-tns-c61-22.ng-star-inserted > div > div.p-datepicker-calendar-container.ng-tns-c61-22.ng-star-inserted > table > tbody > tr:nth-child(1) > td:nth-child(6)'
        browser.find_elements(By.CSS_SELECTOR, dia_actual)[0].click()
        time.sleep(1)

        dropdown = 'body > cts-root > cts-main > div > div.layout-main > div > cts-calendar > p-dialog.p-element.custom-dialog.ng-tns-c34-15.ng-star-inserted > div > div > div.ng-tns-c34-15.p-dialog-content > form > div:nth-child(2) > p-dropdown'
        button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, dropdown)))
        button.click()
        time.sleep(1)

        asiento_0906 = '#pr_id_11_list > p-dropdownitem:nth-child(29)'
        browser.find_elements(By.CSS_SELECTOR, asiento_0906)[0].click()
        time.sleep(1)

        guardar_selec = 'body > cts-root > cts-main > div > div.layout-main > div > cts-calendar > p-dialog.p-element.custom-dialog.ng-tns-c34-15.ng-star-inserted > div > div > div.p-dialog-footer.ng-tns-c34-15.ng-star-inserted > button.p-element.p-ripple.p-button-raised.p-button-sm.p-button-success.p-button.p-component.ng-star-inserted'
        browser.find_elements(By.CSS_SELECTOR, guardar_selec)[0].click()
        time.sleep(1)

        aceptar_boton = 'body > cts-root > cts-main > div > div.layout-main > div > cts-calendar > cts-core-messages > p-dialog > div > div > div.p-dialog-footer.ng-tns-c34-21.ng-star-inserted > button'
        browser.find_elements(By.CSS_SELECTOR, aceptar_boton)[0].click()


Main_bot()