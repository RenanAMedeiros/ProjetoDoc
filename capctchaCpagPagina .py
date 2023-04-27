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
from bs4 import BeautifulSoup
import xlsxwriter





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



#diretorio planilha de salvar resultados
nomeCaminhoArquivoFinal = "C:\\Users\\41348200812\\Desktop\\projetoDoc\\Analitico_SDP.xlsx"
planilhaCriada = xlsxwriter.Workbook(nomeCaminhoArquivoFinal)
sheet1 = planilhaCriada.add_worksheet()

#cria header
sheet1.write("A1", "Placa")
sheet1.write("B1", "Renavam")
sheet1.write("C1", "Chassi")
sheet1.write("D1", "Pesquisa_Concluída")
sheet1.write("E1", "Valor")

tabela=pd.read_excel("Analitico_SDP.xlsx")

# Acessando o Site Fazendo
navegador.get("https://cpag.prf.gov.br/nada_consta/index.jsf")
navegador.maximize_window()
time.sleep(3)
placa_input = navegador.find_element(By.ID,value= "formConsultarExterno:placa")
sleep(3)
renavam_input = navegador.find_element(By.ID,value= "formConsultarExterno:renavam")
sleep(3)
placa_input.clear()
renavam_input.clear()
placa_input.send_keys("FAT6J05")
renavam_input.send_keys("1272775590")

chave_capctcha = navegador.find_element(By.ID,value='captcha').get_attribute('data-sitekey')


solver = recaptchaV2Proxyless ()
solver.set_verbose(1)
solver.set_key(chave_api)
solver.set_website_url("https://cpag.prf.gov.br/nada_consta/index.jsf")
solver.set_website_key(chave_capctcha)


resposta=solver.solve_and_return_solution()

navegador.execute_script(f"document.getElementById('g-recaptcha-response').value='{resposta}'")
elemento = navegador.find_element(By.XPATH,value='//a[@onclick="mojarra.jsfcljs(document.getElementById(\'formConsultarExterno\'),{\'formConsultarExterno:j_idt72\':\'formConsultarExterno:j_idt72\'},\'\');return false"]')

# Execute o código JavaScript associado ao atributo onclick
navegador.execute_script(elemento.get_attribute('onclick'))
html = '<div class="ui-dialog-content ui-widget-content" style="height: auto;"><ul id="formConsultarExterno:msgErro" class="msgErro"><li>	Placa ou RENAVAM não conferem. </li></ul></div>'
soup = BeautifulSoup(html, 'html.parser')
li_tag = soup.find('li')
texto = li_tag.get_text(strip=True)
resultado = texto




if texto == 'Placa ou RENAVAM não conferem.':
    sleep(3)
    #formConsultarExterno:j_idt57

   
    
    navegador.find_element(By.ID,value='formConsultarExterno:j_idt57').click()


else:
    print('Caso Encontrado.')



print(resultado)
sleep(5)



if resposta != 0:
    print(resposta)
    #preencher o campo do token do captcha
    #g-recaptcha-response
    #conteudoPaginaPlaceHolder_btn_Consultar
else:
    print(solver.err_string)    

sleep(4)

