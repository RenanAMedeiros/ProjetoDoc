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
from selenium import webdriver as navegador
import openpyxl as workbook
import os
import win32com.client as win32
import re
df = pd.read_excel("Consulta_SDPWIN.xlsx")
 
# Tratando o arquivo importado .xlsx
 
df_ajustado = df[['Placa','Chassi','Renavam','UF','Procedencia','DataEmissaoCRV','DataEmissaoCRLV','Exercicio',
                  'Cor','MarcaModelo','Combustivel','Categoria','Carroceria','Especie','Tipo','AnoFabricacao',
                  'AnoModelo','CapPassageiro','NumMotor','Nome','Documento','NomeAnterior','IPVA_Licen','Multas',
                  'TotalIPVA','TotalLicen','TotalDPVAT','Dersa','Der','Detran','Cetesb','Renainf','Municipais',
                  'PRF','TotalMultas','CV_ComunicVenda','CV_Inclusao','CV_TipoComprador','CV_DocComprador','CV_DataVenda',
                  'CV_NotaFiscal','CV_Protocolo','IG_CodFinanceira','IG_NomeFinanceira','IG_DocProprietario','IG_NomeProprietario',
                  'IG_Inclusao','IG_NumContrato','IG_VigenciaContrato','IG_TipoTransacao','IG_TipoRestricao','G_RestricaoFinanceira1',
                  'G_RestricaoFinanceira2','G_RestricaoFinanceira3','G_RestricaoFinanceira4','G_CodFinanceira','G_NomeFinanceira',
                  'G_DocProprietario','G_NomeProprietario','G_Inclusao','G_NumContrato','G_VigenciaContrato','G_TipoTransacao',
                  'G_TipoRestricao','OrgaoAutuador','Infracao','NumAutoInfracao','DataInfracao','Valor','ValorPago','Furto',
                  'Guincho','Administrativa','Judicial','Tributaria','Renajud']]

print(df_ajustado)

# Iniciando Biblioteca Webdriver para iniciar o navegador
navegador = webdriver.Chrome()

# Acessando o Site Fazendo
navegador.get("https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx")

chave_capctcha = navegador.find_element(By.ID,'conteudoPaginaPlaceHolder_g_recaptcha').get_attribute('data-sitekey')


solver = recaptchaV2Proxyless ()
solver.set_verbose(1)
solver.set_key(chave_api)
solver.set_website_url("https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx")
solver.set_website_key(chave_capctcha)

resposta=solver.solve_and_return_solution()

if resposta != 0:
    print(resposta)
    #preencher o campo do token do captcha
    #g-recaptcha-response
    #conteudoPaginaPlaceHolder_btn_Consultar
    
    navegador.execute_script(f"document.getElementById('g-recaptcha-response').value='{resposta}'")
else:
    print(solver.err_string)    

sleep(4)

# Iterando informações sobre a coluna "Placa" "Renavam" e enviando cada valor individualmente(por linha matriz)
for placa, renavam in zip(df_ajustado['Placa'], df_ajustado['Renavam']):
    sleep(3)
    try:
        placa_input = navegador.find_element(By.ID, "conteudoPaginaPlaceHolder_txtPlaca")
        sleep(3)
        renavam_input = navegador.find_element(By.ID, "conteudoPaginaPlaceHolder_txtRenavam")
        sleep(3)
        placa_input.clear()
        renavam_input.clear()
        placa_input.send_keys(placa)
        renavam_input.send_keys(renavam)
        chave_capctcha = navegador.find_element(By.ID,'conteudoPaginaPlaceHolder_g_recaptcha').get_attribute('data-sitekey')
        solver = recaptchaV2Proxyless ()
        solver.set_verbose(1)
        solver.set_key(chave_api)
        solver.set_website_url("https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx")
        solver.set_website_key(chave_capctcha)
        resposta=solver.solve_and_return_solution()
        navegador.execute_script(f"document.getElementById('g-recaptcha-response').value='{resposta}'")
        navegador.find_element(By.ID,'conteudoPaginaPlaceHolder_btn_Consultar').click()
        sleep(120)
        navegador.get("https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx")

        # Aguardar o carregamento dos resultados da busca
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ID_DO_ELEMENTO_DOS_RESULTADOS_DA_BUSCA")))
        
        # Adicione aqui o código para capturar os resultados da busca e fazer o que for necessário com eles
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}. Reiniciando o loop.")
        navegador.refresh()
        continue

