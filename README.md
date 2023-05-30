# Web Crawler para raspagem de dados do Mercado Livre
Este projeto é construído em Python e utiliza o framework Selenium realizar a raspagem de dados da página de ofertas do Mercado Livre. O web crawler extrai informações como nome do produto, valor atual, valor antigo, valor total, desconto, link da imagem, prazo de frete e nome da loja vendedora (se disponível). Os dados extraídos são exportados em formato JSON.

## Antes de executar o projeto
Verifique se você possui as seguintes dependências instaladas em seu ambiente de desenvolvimento:
- Python 3.11.2
- Selenium 4.9.1

Recomendo criar um ambiente virtual com o módulo venv (mais informações aqui: https://docs.python.org/pt-br/3/library/venv.html) para evitar conflitos de versões caso já possua as dependências instaladas em sua máquina.
 
Versão do ChromeDriver utilizada:
- ChromeDriver 113.0.5672.63

O ChromeDriver pode ser baixado neste link:
https://chromedriver.chromium.org/downloads.
Baixe a mesma versão do seu navegador.

## Executando o projeto
Para rodar o programa navegue até a pasta do projeto, abra o terminal nessa pasta e use o seguinte comando:
  
    python script_mercadolivre.py
 obs: não esqueça de ativar o ambiente virtual antes de executar o comando acima, caso tenha decidido utilizar :)
