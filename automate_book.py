import select
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

def credenciales():
    creds = {'usuario1':'gerardo.rodriguezv@ab-inbev.com', 'pass1':'Cerveza.inbev!'}

    return creds

def filling_web():

    creds = credenciales()
    # ------------------------------------------------------------------------------------------------
    correo_login = 'body > cts-root > cts-login > div > div > form > input'
    pass_login = 'body > cts-root > cts-login > div > div > form > p-password > div > input'
    boton_login = 'body > cts-root > cts-login > div > div > form > button'
    boton_reservar = 'body > cts-root > cts-main > div > div.layout-main > div > div > div > div > div > div > div:nth-child(3) > button'
    reserva_calendario = 'body > cts-root > cts-main > div > div.layout-main > div > div > div > div > div > div > div:nth-child(3) > p-menu > div > ul > li:nth-child(1)'
    reserva_mapa = 'body > cts-root > cts-main > div > div.layout-main > div > div > div > div > div > div > div:nth-child(3) > p-menu > div > ul > li:nth-child(2) > a'
    seleccion_dia = 'body > cts-root > cts-main > div > div.layout-main > div > cts-seats > div.grid > div > div > div.flex.card-container.grid > div:nth-child(1) > p-calendar > span > input'
    # ------------------------------------------------------------------------------------------------

    boton_apartar_dia = 'body > cts-root > cts-main > div > div.layout-main > div > cts-calendar > div > div > div > div > div:nth-child(1) > button:nth-child(1)'
    selecc_dia_b = 'body > cts-root > cts-main > div > div.layout-main > div > cts-calendar > p-dialog.p-element.custom-dialog.ng-tns-c34-15.ng-star-inserted > div > div > div.ng-tns-c34-15.p-dialog-content > form > div:nth-child(1) > p-calendar > span > button'
    selecc_dia_t = 'body > cts-root > cts-main > div > div.layout-main > div > cts-calendar > p-dialog.p-element.custom-dialog.ng-tns-c34-34.ng-star-inserted > div > div > div.ng-tns-c34-34.p-dialog-content > form > div:nth-child(1) > p-calendar > span > input'
    calendar_days = 'body > div.ng-trigger.ng-trigger-overlayAnimation.ng-tns-c61-22.p-datepicker.p-component.p-datepicker-touch-ui.ng-star-inserted'
    # ------------------------------------------------------------------------------------------------

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome('.\\selenium_chrome\\chromedriver.exe', chrome_options=chrome_options)
    # ------------------------------------------------------------------------------------------------

    driver.maximize_window()
    driver.get(url='https://cts-appp.herokuapp.com/#/login')
    driver.find_element_by_css_selector(correo_login).send_keys(creds['usuario1'])
    driver.find_element_by_css_selector(pass_login).send_keys(creds['pass1'])
    driver.find_element_by_css_selector(boton_login).click()

    time.sleep(3)

    driver.find_element_by_css_selector(boton_reservar).click()

    def mapa():
        driver.find_element_by_css_selector(reserva_mapa).click()

    def calendario():
        dia = '03/12/2022'
        driver.find_element_by_css_selector(reserva_calendario).click()
        time.sleep(3)

        driver.find_element_by_css_selector(boton_apartar_dia).click()
        time.sleep(1)
        driver.find_element_by_css_selector(selecc_dia_b).click()

        sig_mes = 'body > div.ng-trigger.ng-trigger-overlayAnimation.ng-tns-c61-22.p-datepicker.p-component.p-datepicker-touch-ui.ng-star-inserted > div.p-datepicker-group-container.ng-tns-c61-22.ng-star-inserted > div > div.p-datepicker-header.ng-tns-c61-22 > button.p-ripple.p-element.p-datepicker-next.p-link.ng-tns-c61-22'
        driver.find_element_by_css_selector(sig_mes).click()

        dia = 'body > div.ng-trigger.ng-trigger-overlayAnimation.ng-tns-c61-22.p-datepicker.p-component.p-datepicker-touch-ui.ng-star-inserted > div.p-datepicker-group-container.ng-tns-c61-22.ng-star-inserted > div > div.p-datepicker-calendar-container.ng-tns-c61-22.ng-star-inserted > table > tbody > tr:nth-child(5) > td:nth-child(3)'
        sabado = 'body > div.ng-trigger.ng-trigger-overlayAnimation.ng-tns-c61-22.p-datepicker.p-component.p-datepicker-touch-ui.ng-star-inserted > div.p-datepicker-group-container.ng-tns-c61-22.ng-star-inserted > div > div.p-datepicker-calendar-container.ng-tns-c61-22.ng-star-inserted > table > tbody > tr:nth-child(1) > td:nth-child(6)'
        driver.find_element_by_css_selector(sabado).click()

        ubi_menu = 'body > cts-root > cts-main > div > div.layout-main > div > cts-calendar > p-dialog.p-element.custom-dialog.ng-tns-c34-15.ng-star-inserted > div > div > div.ng-tns-c34-15.p-dialog-content > form > div:nth-child(2) > p-dropdown > div > div.p-dropdown-trigger.ng-tns-c58-23'

        driver.find_element_by_css_selector(ubi_menu).click()

        ubi_text = 'body > div > div.p-dropdown-header.ng-tns-c58-23.ng-star-inserted > div > input'
        driver.find_element_by_css_selector(ubi_text).send_keys('BIT 0906')

        print('ID', driver.find_elements_by_id('pr_id_12_label'))
        driver.find_elements_by_id('pr_id_12_label')[0].send_keys('BIT 0906')
        #select_dropdown.select_by_value('BIT 0906')

        ubi_guardar = 'body > cts-root > cts-main > div > div.layout-main > div > cts-calendar > p-dialog.p-element.custom-dialog.ng-tns-c34-38.ng-star-inserted > div > div > div.p-dialog-footer.ng-tns-c34-38.ng-star-inserted > button.p-element.p-ripple.p-button-raised.p-button-sm.p-button-success.p-button.p-component.ng-star-inserted'
        driver.find_element_by_css_selector(ubi_guardar).click()


    calendario()




filling_web()