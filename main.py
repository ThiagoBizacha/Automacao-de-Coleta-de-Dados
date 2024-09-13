import requests
from lxml import html
import pandas as pd
import time
import re
from datetime import datetime
import logging
import random
import os

# Diretório para salvar os logs
log_directory = "C:/Users/ThiagoBizacha/Desktop/Projeto_Automacao_Coleta_Dados/logs/"
os.makedirs(log_directory, exist_ok=True)  # Cria o diretório se não existir

# Configuração do logging para salvar no diretório especificado
logging.basicConfig(
    filename=os.path.join(log_directory, 'amazon_scraper.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Função para obter os links das categorias da página inicial
def get_category_links(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao acessar a URL {url}: {e}")
        return []

    tree = html.fromstring(response.content)
    categories = tree.xpath('//div[contains(@class, "_p13n-zg-nav-tree-all_style_zg-browse-group__88fbz")]//a')
    category_links = [{'category': cat.text_content().strip(), 'link': 'https://www.amazon.nl' + cat.get('href')} for cat in categories]

    return category_links

# Função para extrair detalhes dos produtos
def extract_product_details(items, category):
    products = []
    today_date = datetime.today().strftime('%Y-%m-%d')

    for index, item in enumerate(items, start=1):
        product_id = item.xpath('.//@data-asin')
        product_id = product_id[0] if product_id else "No ID"

        position = item.xpath('.//span[@class="zg-bdg-text"]/text()')
        position = position[0].strip() if position else str(index)

        image = item.xpath('.//img[contains(@class, "a-dynamic-image")]/@src')
        image_link = image[0] if image else "No image link"

        title = item.xpath('.//a/span/div/text()')
        title = title[0].strip() if title else "No title"

        link = item.xpath('.//a[contains(@class, "a-link-normal")]/@href')
        product_link = "https://www.amazon.nl" + link[0] if link else "No product link"

        name = item.xpath('.//a[@class="a-link-normal aok-block"]/@href')
        name = name[0].split('/')[1] if name else "No name"

        rating = item.xpath('.//span[contains(@class, "a-icon-alt")]/text()')
        rating = rating[0].strip() if rating else "No rating"

        reviews = item.xpath('.//span[@class="a-size-small"]/text()')
        reviews = reviews[0].strip() if reviews else "No reviews"

        price = item.xpath('.//span[contains(@class, "p13n-sc-price")]/text()')
        if price:
            price = price[0].strip()
            currency_symbol = ''.join(re.findall(r'[^\d.,]', price))
            value = ''.join(re.findall(r'[\d.,]+', price))
        else:
            currency_symbol = "Not Available"
            value = "Not Available"

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

    return products

# Função que obtém produtos com retries
def get_amazon_bestsellers(url, category, retries=5, backoff_factor=0.3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao acessar {url} na tentativa {i+1}/{retries}: {e}")
            time.sleep(backoff_factor * (2 ** i))
        if i == retries - 1:
            return []

    tree = html.fromstring(response.content)
    items = tree.xpath('//div[contains(@id, "p13n-asin-index")]')
    logging.info(f"Encontrados {len(items)} itens na categoria {category}.")

    return extract_product_details(items, category)

# Função para salvar os dados em Excel
def save_to_excel(products, directory_path, category_type):
    if not products:
        logging.warning(f"Nenhum produto encontrado para a categoria {category_type}.")
        return

    df = pd.DataFrame(products)
    today_date = datetime.today().strftime('%Y-%m-%d')
    filename = f"{directory_path}/bot_amazon_{category_type}_{today_date}.xlsx"
    df.to_excel(filename, index=False)
    logging.info(f"Produtos salvos em {filename}")

# Função que processa uma categoria específica
def process_category(category_url, category_type, directory_path):
    """
    Faz o processamento completo da categoria, coletando e salvando os dados.

    Parâmetros:
        category_url (str): URL da categoria (ex: Best Sellers)
        category_type (str): Tipo de categoria (ex: best_sellers, movers_and_shakers)
        directory_path (str): Caminho para salvar o Excel
    """
    # Obtém links das subcategorias
    category_links = get_category_links(category_url)
    all_products = []

    for category_link in category_links:
        category = category_link['category']
        link = category_link['link']
        logging.info(f"Processando categoria: {category}")
        
        # Extrai os produtos de cada subcategoria
        products = get_amazon_bestsellers(link, category)
        all_products.extend(products)
        
        # Intervalo aleatório para evitar sobrecarga no servidor
        time.sleep(random.uniform(5, 10))

    # Salva os produtos extraídos em um arquivo Excel
    save_to_excel(all_products, directory_path, category_type)

# Função principal
if __name__ == "__main__":
    directory_path = "C:/Users/ThiagoBizacha/Desktop/Projeto_Automacao_Coleta_Dados/data/output/bot_amazon"

    base_url_bestsellers = "https://www.amazon.nl/gp/bestsellers/"
    process_category(base_url_bestsellers, "best_sellers", directory_path)

    base_url_movers_shakers = "https://www.amazon.nl/gp/movers-and-shakers/"
    process_category(base_url_movers_shakers, "movers_and_shakers", directory_path)

    base_url_new_releases = "https://www.amazon.nl/gp/new-releases/"
    process_category(base_url_new_releases, "new_releases", directory_path)

    logging.info("Processo finalizado!")
    print("Finalizado!")
