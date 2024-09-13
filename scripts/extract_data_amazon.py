import requests  # Biblioteca para fazer requisições HTTP, usada para acessar as páginas da Amazon
from lxml import html  # Biblioteca para parsing de HTML, usada para extrair informações de páginas
import pandas as pd  # Biblioteca para manipulação de dados, usada para criar e manipular DataFrames
import time  # Biblioteca para gerenciar o tempo, usada para controlar intervalos entre requisições
import re  # Biblioteca de expressões regulares, usada para manipulação de strings
from datetime import datetime  # Biblioteca para manipular datas, usada para adicionar data aos dados
import logging  # Biblioteca para criação de logs, usada para registrar eventos e erros
import random  # Biblioteca para gerar números aleatórios, usada para intervalos aleatórios entre requisições
import os  # Biblioteca para manipulação de sistemas operacionais, usada para criar diretórios

# Diretório para salvar os logs
log_directory = "C:/Users/ThiagoBizacha/Desktop/Projeto_Automacao_Coleta_Dados/logs/"
os.makedirs(log_directory, exist_ok=True)  # Cria o diretório de logs se ele ainda não existir

# Configuração do logging para salvar no diretório especificado
logging.basicConfig(
    filename=os.path.join(log_directory, 'amazon_scraper.log'),  # Define o nome e local do arquivo de log
    level=logging.INFO,  # Define o nível de log (INFO), para registrar eventos gerais
    format='%(asctime)s - %(levelname)s - %(message)s'  # Define o formato da mensagem de log: data/hora, nível e mensagem
)

logging.info(f"Extração iniciada")  

# Função para obter os links das categorias da página inicial (Elektronica, Software ou Boeken)
def get_category_links(url):
    """
    Faz uma requisição à página principal e extrai os links das categorias.
    
    Parâmetros:
        url (str): URL da página principal da Amazon (ex: Best Sellers)

    Retorno:
        list: Lista de dicionários contendo o nome e o link completo de cada categoria
    """
    # Define o cabeçalho da requisição para simular um navegador e evitar bloqueios
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    try:
        # Faz a requisição à URL com o cabeçalho definido
        response = requests.get(url, headers=headers, timeout=10)  # Timeout de 10 segundos para evitar travamentos
        response.raise_for_status()  # Gera um erro se o status da requisição for diferente de 200 (OK)
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao acessar a URL {url}: {e}")  # Registra o erro nos logs
        return []  # Retorna uma lista vazia caso haja falha na requisição

    # Faz o parsing do conteúdo HTML da página
    tree = html.fromstring(response.content)
    
    # Usa XPath para encontrar os links das categorias
    categories = tree.xpath('//div[contains(@class, "_p13n-zg-nav-tree-all_style_zg-browse-group__88fbz")]//a')
    
    # Cria uma lista de dicionários contendo o nome e o link completo de cada categoria
    category_links = [{'category': cat.text_content().strip(), 'link': 'https://www.amazon.nl' + cat.get('href')} for cat in categories]

    return category_links  # Retorna a lista de categorias

# Função para extrair detalhes dos produtos de uma categoria específica
def extract_product_details(items, category):
    """
    Extrai detalhes dos produtos de uma categoria (ex: Best Sellers, Movers and Shakers).

    Parâmetros:
        items (list): Lista de elementos de produtos extraídos da página da categoria
        category (str): Nome da categoria de produtos

    Retorno:
        list: Lista de dicionários contendo os detalhes de cada produto
    """
    products = []  # Lista onde serão armazenados os detalhes dos produtos
    today_date = datetime.today().strftime('%Y-%m-%d')  # Data atual formatada para ser usada em cada produto

    # Itera sobre cada item da lista de produtos
    for index, item in enumerate(items, start=1):
        # Extrai o ID do produto (ASIN)
        product_id = item.xpath('.//@data-asin')
        product_id = product_id[0] if product_id else "No ID"  # Usa "No ID" caso o ID não seja encontrado

        # Extrai a posição no ranking (por exemplo, #1, #2, etc.)
        position = item.xpath('.//span[@class="zg-bdg-text"]/text()')
        position = position[0].strip() if position else str(index)  # Se a posição não estiver disponível, usa o índice do loop

        # Extrai o link da imagem do produto
        image = item.xpath('.//img[contains(@class, "a-dynamic-image")]/@src')
        image_link = image[0] if image else "No image link"  # Caso não haja imagem, usa "No image link"

        # Extrai o título do produto
        title = item.xpath('.//a/span/div/text()')
        title = title[0].strip() if title else "No title"  # Se não houver título, usa "No title"

        # Extrai o link do produto
        link = item.xpath('.//a[contains(@class, "a-link-normal")]/@href')
        product_link = "https://www.amazon.nl" + link[0] if link else "No product link"

        # Extrai o nome do produto (parte da URL)
        name = item.xpath('.//a[@class="a-link-normal aok-block"]/@href')
        name = name[0].split('/')[1] if name else "No name"

        # Extrai a classificação/avaliação do produto
        rating = item.xpath('.//span[contains(@class, "a-icon-alt")]/text()')
        rating = rating[0].strip() if rating else "No rating"

        # Extrai o número de avaliações (quantidade de reviews)
        reviews = item.xpath('.//span[@class="a-size-small"]/text()')
        reviews = reviews[0].strip() if reviews else "No reviews"

        # Extrai o preço do produto
        price = item.xpath('.//span[contains(@class, "p13n-sc-price")]/text()')
        if price:
            price = price[0].strip()
            currency_symbol = ''.join(re.findall(r'[^\d.,]', price))  # Extrai o símbolo da moeda
            value = ''.join(re.findall(r'[\d.,]+', price))  # Extrai o valor numérico do preço
        else:
            currency_symbol = "Not Available"
            value = "Not Available"

        # Adiciona os detalhes do produto à lista de produtos
        products.append({
            "category": category,
            "rank": position,
            "asin": product_id,
            "name": name,
            "title": title,
            "rating": rating,
            "reviews": reviews,
            "symbol": currency_symbol,
            "value": value,
            "image": image_link,
            "link": product_link,        
            "date": today_date
        })

    return products  # Retorna a lista de produtos

# Função que obtém os produtos mais vendidos em uma categoria específica, com retries para evitar falhas temporárias
def get_amazon_bestsellers(url, category, retries=5, backoff_factor=0.3):
    """
    Faz a requisição para uma categoria específica da Amazon e coleta os produtos. Tenta novamente em caso de falhas.

    Parâmetros:
        url (str): URL da categoria da Amazon
        category (str): Nome da categoria de produtos (Best Sellers, Movers and Shakers, etc.)
        retries (int): Número máximo de tentativas de requisição
        backoff_factor (float): Fator de tempo para espera entre retries

    Retorno:
        list: Lista de produtos da categoria, ou lista vazia em caso de falha
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Loop para realizar retries em caso de falha na requisição
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)  # Faz a requisição com um timeout de 10 segundos
            response.raise_for_status()  # Gera um erro se o status não for 200 (OK)
            break  # Se a requisição for bem-sucedida, sai do loop
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao acessar {url} na tentativa {i+1}/{retries}: {e}")  # Registra o erro nos logs
            time.sleep(backoff_factor * (2 ** i))  # Aumenta o tempo de espera exponencialmente (backoff)
        if i == retries - 1:
            return []  # Retorna lista vazia após o número máximo de retries

    # Faz o parsing do conteúdo da página
    tree = html.fromstring(response.content)
    
    # Extrai os produtos da categoria com base no identificador "p13n-asin-index"
    items = tree.xpath('//div[contains(@id, "p13n-asin-index")]')
    logging.info(f"Encontrados {len(items)} itens na categoria {category}.")

    # Retorna os detalhes dos produtos extraídos
    return extract_product_details(items, category)

# Função para salvar os dados consolidados em Excel
def save_to_excel_consolidated(products, directory_path):
    """
    Salva os produtos extraídos em um único arquivo Excel consolidado.

    Parâmetros:
        products (list): Lista de produtos de todas as categorias
        directory_path (str): Caminho para salvar o arquivo Excel
    """
    if not products:
        logging.warning("Nenhum produto encontrado nas categorias.")  # Registra um aviso se não houver produtos
        return

    # Cria um DataFrame a partir da lista de produtos
    df = pd.DataFrame(products)
    
    # Define o nome do arquivo com base na data atual
    today_date = datetime.today().strftime('%Y-%m-%d')
    filename = f"{directory_path}/extract_amazon_full_{today_date}.xlsx"
    
    # Salva o DataFrame em um arquivo Excel
    df.to_excel(filename, index=False)
    logging.info(f"Dados consolidados salvos em {filename}")  # Registra a conclusão da tarefa

# Função que processa uma categoria específica e adiciona a coluna "origin"
def process_category(category_url, category_type):
    """
    Processa uma categoria específica, extrai os produtos e adiciona uma coluna "origin" para identificar a origem.

    Parâmetros:
        category_url (str): URL da categoria
        category_type (str): Tipo de categoria (ex: Best Sellers, Movers and Shakers)

    Retorno:
        list: Lista de produtos com a coluna "origin" indicando a origem dos dados
    """
    # Obtém os links das subcategorias
    category_links = get_category_links(category_url)
    all_products = []

    # Processa cada subcategoria
    for category_link in category_links:
        category = category_link['category']  # Nome da subcategoria
        link = category_link['link']  # Link da subcategoria
        logging.info(f"Processando categoria: {category}")
        
        # Extrai os produtos da subcategoria
        products = get_amazon_bestsellers(link, category)
        
        # Adiciona a origem dos dados na coluna "origin"
        for product in products:
            product['origin'] = category_type  # Adiciona a origem (ex: best_sellers)
        
        all_products.extend(products)  # Adiciona os produtos à lista geral
        
        # Pausa com intervalo aleatório para evitar sobrecarga no servidor
        time.sleep(random.uniform(1, 3))

    return all_products  # Retorna a lista de produtos processados

# Função principal que coordena todo o processo
def extract_data():
    print("extração iniciada")

    directory_path = "C:/Users/ThiagoBizacha/Desktop/Projeto_Automacao_Coleta_Dados/data/output/bot_amazon"

    # Lista para armazenar os produtos de todas as categorias
    all_products = []

    # Processa Best Sellers e adiciona à lista consolidada
    base_url_bestsellers = "https://www.amazon.nl/gp/bestsellers/"
    all_products.extend(process_category(base_url_bestsellers, "best_sellers"))

    # Processa Movers and Shakers e adiciona à lista consolidada
    base_url_movers_shakers = "https://www.amazon.nl/gp/movers-and-shakers/"
    all_products.extend(process_category(base_url_movers_shakers, "movers_and_shakers"))

    # Processa New Releases e adiciona à lista consolidada
    base_url_new_releases = "https://www.amazon.nl/gp/new-releases/"
    all_products.extend(process_category(base_url_new_releases, "new_releases"))

    # Cria um DataFrame com todos os produtos
    df_consolidated = pd.DataFrame(all_products)

    # Exibe o DataFrame final para visualização
    #print(df_final)

    # Salva todos os dados consolidados em um arquivo Excel único
    save_to_excel_consolidated(all_products, directory_path)

    logging.info("Processo finalizado!")  # Registra a finalização do processo
    print("extração finalizada")

    return df_consolidated

#if __name__ == "__main__":
 #   extract_data()
