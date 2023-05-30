import time
import json
import codecs
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")


browser = webdriver.Chrome(options=chrome_options)


#Entra na pagina do mercado livre
browser.get('https://www.mercadolivre.com.br/ofertas')
time.sleep(2)
page_home = BeautifulSoup(browser.page_source, 'html.parser') 


# Encontra o input para calcular o frete
browser.find_element(By.XPATH, '/html/body/header/div/div[4]/div/a/span').click()
time.sleep(2)


iframe = browser.find_element(By.XPATH, '/html/body/div[4]/div[1]/iframe')
browser.switch_to.frame(iframe) # Mudando o foco para o iframe para preencher o CEP
time.sleep(1)
cep = browser.find_element(By.XPATH, '//*[@id="addressesForm"]/div/div/div/div[1]/label/div/input') # Seleciona o campo de input
cep.send_keys('65054560') # Preenche o CEP
time.sleep(1)
browser.find_element(By.XPATH,'//*[@id="addressesForm"]/div/div/div/div[1]/label/div/div/button').click() # Confirma o CEP
time.sleep(2)
browser.switch_to.default_content() # Sai do iframe e retorna para a pagina principal


#Aceita politica de cookies
browser.find_element(By.XPATH,'/html/body/div[2]/div[1]/div/div[3]/button[1]').click()


product = {'name': [], 'price_old': [], 'price_now': [], 'discount': [], 'shipping_deadline': [], 'link_img': [], 'name_seller': []}


for page_number in range(1,21):
    
    print('pagina atual: ', page_number)
    time.sleep(1)
    for i in range(48):
        # Navega até o produto
        time.sleep(1)
        browser.find_element(By.XPATH,f'//*[@id="root-app"]/div[2]/div[2]/div/ol/li[{i+1}]/div/a/div/div[1]/img').click()
       
       
        # Pega o html da pagina com as informações
        time.sleep(2)
        page_product = BeautifulSoup(browser.page_source, 'html.parser') 


        time.sleep(1)
        # Coleta o nome do produto
        product_nome = page_product.find('h1', class_='ui-pdp-title').text
        product['name'].append(product_nome)
        print(product_nome)
        

        # Coleta preço atual do produto
        time.sleep(1)
        card_product_price = page_product.find('div', class_='ui-pdp-price__second-line')
        product_price_now = card_product_price.find('span', class_='andes-money-amount__fraction').text # Coleta o preço atual
        product['price_now'].append(product_price_now)

        
        time.sleep(1)
        # Coleta preço antigo do produto
        product_price_old_container = page_product.find('s', 'andes-money-amount ui-pdp-price__part ui-pdp-price__original-value andes-money-amount--previous andes-money-amount--cents-superscript andes-money-amount--compact')
        product_price_old = product_price_old_container.find('span','andes-money-amount__fraction').text
        if product_price_old is not None:
            product['price_old'].append(product_price_old)
        else:
            product['price_old'].append('Sem preço anterior')


        # Coleta o desconto do produto
        product_discount = page_product.find('span', class_=['andes-money-amount__discount','andes-money-amount ui-pdp-price__part andes-money-amount--cents-comma andes-money-amount--compact']).text
        if product_discount is not None:
            product['discount'].append(product_discount)
        else:
            product['discount'].append('Não possui desconto')


        # Coleta o prazo de entrega
        shipping_deadline = page_product.find('p', class_=['ui-pdp-color--GREEN ui-pdp-family--REGULAR ui-pdp-media__title ui-pdp-media__title--on-hover', 'ui-pdp-media__title--on-hover','ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-media__title', 'ui-pdp-media__title ui-pdp-media__title--on-hover', 'ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-media__title ui-pdp-media__title--on-hover', 'ui-pdp-color--BLACK ui-pdp-family--REGULAR ui-pdp-media__title', 'ui-pdp-color--GREEN ui-pdp-family--REGULAR ui-pdp-media__title', 'ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--SEMIBOLD ui-pdp-stock-information__title']).text
        if shipping_deadline is not None:
            # Caso não encontre uma dessas classes informando o prazo, o else irá verificar quanto a disponibilidade do produto
            product['shipping_deadline'].append(shipping_deadline)
        else:
            shipping_deadline = page_product.find('div', class_= 'andes-message__content andes-message__content--untitled')
            if shipping_deadline.text == 'Por enquanto, não podemos fazer envios para essa localização.':
                shipping_deadline = page_product.find('div', class_= 'andes-message__content andes-message__content--untitled').text
                product['shipping_deadline'].append(shipping_deadline)
            else:
                product['shipping_deadline'].append('Produto não disponível')


        # Link da imagem
        img = page_product.find('img', class_='ui-pdp-image ui-pdp-gallery__figure__image')
        product['link_img'].append(img['src'])
        time.sleep(1)


        # Nome da loja vendendora
        name_seller = page_product.find('div', class_='ui-pdp-seller__header__title')
        # Extrai o nome da loja, caso não exista será informado que não há nome da loja vendedora 
        if name_seller is not None:
            product['name_seller'].append(name_seller.text)
        else:
            product['name_seller'].append('Sem nome explícito da loja vendedora')


        # Salva os dados em um json
        with codecs.open("dados.json", "w", encoding='utf-8') as file:
            json.dump(product, file, ensure_ascii=False)
        

        # Sai da página do produto atual e retorna para a página com todos os produtos
        browser.back()


    # Percorre as páginas 
    browser.get(f'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1&page={page_number+1}')
    

# Encerra o navegador após a coleta dos dados
browser.quit()

