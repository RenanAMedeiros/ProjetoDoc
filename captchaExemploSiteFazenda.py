import pandas as pd
from selenium import webdriver
from time import sleep
from openpyxl import load_workbook
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from anticaptchaofficial.recaptchav2proxyless import *
from chave import chave_api

# Iniciando Biblioteca Webdriver para iniciar o navegador
navegador = webdriver.Chrome()

# Acessando o Site Fazendo
navegador.get("https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx")


placa_input = navegador.find_element(By.ID, "conteudoPaginaPlaceHolder_txtPlaca")
sleep(3)
renavam_input = navegador.find_element(By.ID, "conteudoPaginaPlaceHolder_txtRenavam")
sleep(3)
placa_input.clear()
renavam_input.clear()
placa_input.send_keys("GEB7J85")
renavam_input.send_keys("1123105879")

chave_capctcha = navegador.find_element(By.ID,'conteudoPaginaPlaceHolder_g_recaptcha').get_attribute('data-sitekey')


solver = recaptchaV2Proxyless ()
solver.set_verbose(1)
solver.set_key(chave_api)
solver.set_website_url("https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx")
solver.set_website_key(chave_capctcha)


resposta=solver.solve_and_return_solution()

navegador.execute_script(f"document.getElementById('g-recaptcha-response').value='{resposta}'")
navegador.find_element(By.ID,'conteudoPaginaPlaceHolder_btn_Consultar').click()


if resposta != 0:
    print(resposta)
    #preencher o campo do token do captcha
    #g-recaptcha-response
    #conteudoPaginaPlaceHolder_btn_Consultar
    
    navegador.execute_script(f"document.getElementById('g-recaptcha-response').value='{resposta}'")
    navegador.find_element(By.ID,'conteudoPaginaPlaceHolder_btn_Consultar').click()
else:
    print(solver.err_string)    

sleep(4)
