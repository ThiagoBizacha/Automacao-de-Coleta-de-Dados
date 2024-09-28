import requests  # Biblioteca para fazer requisições HTTP, usada para acessar as páginas da Amazon
from lxml import html  # Biblioteca para parsing de HTML, usada para extrair informações de páginas
import pandas as pd  # Biblioteca para manipulação de dados, usada para criar e manipular DataFrames
import time  # Biblioteca para gerenciar o tempo, usada para controlar intervalos entre requisições
import re  # Biblioteca de expressões regulares, usada para manipulação de strings
from datetime import datetime  # Biblioteca para manipular datas, usada para adicionar data aos dados
import logging  # Biblioteca para criação de logs, usada para registrar eventos e erros
import random  # Biblioteca para gerar números aleatórios, usada para intervalos aleatórios entre requisições
import os  # Biblioteca para manipulação de sistemas operacionais, usada para criar diretórios
from tqdm import tqdm  # Biblioteca para criar barra de progresso

# Diretório para salvar os logs
log_directory = "C:/Users/ThiagoBizacha/Desktop/Projeto_Automacao_Coleta_Dados/data/logs/"
os.makedirs(log_directory, exist_ok=True)  # Cria o diretório de logs se ele ainda não existir

# Configuração do logging para salvar no diretório especificado
logging.basicConfig(
    filename=os.path.join(log_directory, 'amazon_scraper.log'),  # Define o nome e local do arquivo de log
    level=logging.INFO,  # Define o nível de log (INFO), para registrar eventos gerais
    format='%(asctime)s - %(levelname)s - %(message)s'  # Define o formato da mensagem de log: data/hora, nível e mensagem
)

logging.info(f"Extração iniciada")  

# Função para obter os links das categorias da página inicial (Elektronica, Software ou Boeken)
def get_category_links(url, retries=2, backoff_factor=1):
    """
    Faz uma requisição à página principal e extrai os links das categorias.
    Se falhar em encontrar os links, tenta novamente até 5 vezes.

    Parâmetros:
        url (str): URL da página principal da Amazon (ex: Best Sellers)
        retries (int): Número máximo de tentativas de requisição
        backoff_factor (float): Fator de tempo para espera entre retries

    Retorno:
        list: Lista de dicionários contendo o nome e o link completo de cada categoria
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    for attempt in range(retries):
        try:
            # Faz a requisição à URL com o cabeçalho definido
            response = requests.get(url, headers=headers, timeout=10)  # Timeout de 10 segundos para evitar travamentos
            response.raise_for_status()  # Gera um erro se o status da requisição for diferente de 200 (OK)
            
            # Faz o parsing do conteúdo HTML da página
            tree = html.fromstring(response.content)
            
            # Usa XPath para encontrar os links das categorias
            categories = tree.xpath('//div[contains(@class, "_p13n-zg-nav-tree-all_style_zg-browse-group__88fbz")]//a')
            
            if categories:
                # Cria uma lista de dicionários contendo o nome e o link completo de cada categoria
                category_links = [{'category': cat.text_content().strip(), 'link': 'https://www.amazon.nl' + cat.get('href')} for cat in categories]
                logging.info(f"Links de subcategorias encontrados para a URL: {url}")
                return category_links  # Retorna a lista de categorias
            else:
                # Se não encontrou categorias, tenta novamente
                logging.warning(f"Nenhuma subcategoria encontrada na tentativa {attempt+1}/{retries} para a URL: {url}")
                time.sleep(backoff_factor * (2 ** attempt))  # Espera exponencialmente mais a cada tentativa
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao acessar a URL {url} na tentativa {attempt+1}/{retries}: {e}")
            time.sleep(backoff_factor * (2 ** attempt))  # Espera exponencialmente mais a cada tentativa
    
    logging.error(f"Não foram encontrados links de subcategorias para a URL: {url} após {retries} tentativas.")
    return []  # Retorna uma lista vazia caso haja falha na requisição após o número máximo de tentativas


# Função para extrair detalhes dos produtos de uma categoria específica
import re  # Biblioteca para expressões regulares

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
        position = position[0].strip() if position else 999  # Se a posição não estiver disponível, usa o índice do loop

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

        # Extrai o número do percentual de alta (por exemplo, "427%")
        perc_alta = item.xpath('.//span[contains(@class, "zg-carousel-pct-change")]/text()')
        if perc_alta:
            perc_alta = re.search(r'\d+', perc_alta[0].strip()).group(0)
        else:
            perc_alta = 0

        # Extrai a classificação de vendas completa (exemplo: "Classificação de vendas: 180 (anterior: 950)")
        classificacao_vendas = item.xpath('.//span[contains(@class, "zg-carousel-sales-movement")]/text()')
        classificacao_vendas = classificacao_vendas[0].strip() if classificacao_vendas else "No classificacao vendas"

        # Extrai apenas o número da classificação de vendas (antes dos parênteses) - (por exemplo, "180")
        match_vendas = re.search(r'(\d+)', classificacao_vendas)
        classificacao_vendas_numero = match_vendas.group(1) if match_vendas else 0

        # Extrai apenas o número da classificação de vendas anterior (dentro dos parênteses) - (por exemplo, "950")
        match_vendas_anterior = re.search(r'\((\d+)\)', classificacao_vendas)
        classificacao_vendas_anterior = match_vendas_anterior.group(1) if match_vendas_anterior else 0

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
            "perc_alta": perc_alta,  # Apenas o número do percentual de alta
            "classificacao_vendas": classificacao_vendas_numero,  # Apenas o número da classificação de vendas
            "classificacao_vendas_anterior": classificacao_vendas_anterior,  # Apenas o número da classificação de vendas anterior
            "date": today_date
        })

    return products  # Retorna a lista de produtos

# Função que obtém os produtos mais vendidos em uma categoria específica, com retries para evitar falhas temporárias
def get_amazon_bestsellers(url, category, retries=2, backoff_factor=1):
    """
    Faz a requisição para uma categoria específica da Amazon e coleta os produtos. Tenta novamente em caso de falhas ou
    caso nenhum produto seja encontrado (len(items) == 0).

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

    # Loop para realizar retries em caso de falha na requisição ou no parsing dos itens
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)  # Faz a requisição com um timeout de 10 segundos
            response.raise_for_status()  # Gera um erro se o status não for 200 (OK)
            
            # Faz o parsing do conteúdo da página
            tree = html.fromstring(response.content)
            
            # Extrai os produtos da categoria com base no identificador "p13n-asin-index"
            items = tree.xpath('//div[contains(@id, "p13n-asin-index")]')
            
            # Verifica se foram encontrados itens
            if len(items) > 0:
                logging.info(f"Encontrados {len(items)} itens na categoria {category}.")
                print(f"Encontrados {len(items)} itens na categoria {category}.")
                return extract_product_details(items, category)
            else:
                logging.warning(f"Nenhum item encontrado na categoria {category} na tentativa {i+1}/{retries}.")
                print(f"Nenhum item encontrado na categoria {category} na tentativa {i+1}/{retries}.")
                time.sleep(backoff_factor * (2 ** i))  # Aumenta o tempo de espera exponencialmente (backoff)
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao acessar {url} na tentativa {i+1}/{retries}: {e}")  # Registra o erro nos logs
            time.sleep(backoff_factor * (2 ** i))  # Aumenta o tempo de espera exponencialmente (backoff)
        
        # Se o número máximo de tentativas for atingido e não houver itens, retorna uma lista vazia
        if i == retries - 1:
            logging.error(f"Falha ao obter produtos da categoria {category} após {retries} tentativas.")
            print(f"Falha ao obter produtos da categoria {category} após {retries} tentativas.")
            return []  # Retorna lista vazia após o número máximo de retries

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
        print("Nenhum produto encontrado nas categorias.")
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
    
    if not category_links:
        logging.error(f"Não foram encontrados links de subcategorias para a URL: {category_url}")
        print(f"Não foram encontrados links de subcategorias para a URL: {category_url}")
        return []

    all_products = []

    # Processa cada subcategoria
    for category_link in category_links:
        category = category_link['category']  # Nome da subcategoria
        link = category_link['link']  # Link da subcategoria
        logging.info(f"Processando subcategoria: {category} - {category_type}")
        print(f"Processando subcategoria: {category} - {category_type}")
        
        # Extrai os produtos da subcategoria
        products = get_amazon_bestsellers(link, category)
        
        if not products:
            logging.warning(f"Nenhum produto encontrado na subcategoria: {category} - {category_type}")
        
        # Adiciona a origem dos dados na coluna "origin"
        for product in products:
            product['origin'] = category_type  # Adiciona a origem (ex: best_sellers)
        
        all_products.extend(products)  # Adiciona os produtos à lista geral
        
        # Pausa com intervalo aleatório para evitar sobrecarga no servidor
        time.sleep(random.uniform(10, 20))

    return all_products  # Retorna a lista de produtos processados

# Função principal que coordena todo o processo
def extract_data():
    print("Extração iniciada")

    directory_path = "C:/Users/ThiagoBizacha/Desktop/Projeto_Automacao_Coleta_Dados/data/output/bot_amazon/extract"

    # Lista para armazenar os produtos de todas as categorias
    all_products = []

    # Processa Best Sellers e adiciona à lista consolidada
    logging.info("Iniciando processamento de Best Sellers")
    base_url_bestsellers = "https://www.amazon.nl/gp/bestsellers/"
    best_sellers_products = process_category(base_url_bestsellers, "best_sellers")
    all_products.extend(best_sellers_products)
    logging.info(f"Produtos de Best Sellers: {len(best_sellers_products)}")

    # Pausa com intervalo aleatório para evitar sobrecarga no servidor
    time.sleep(random.uniform(5, 10))

    # Processa Movers and Shakers e adiciona à lista consolidada
    logging.info("Iniciando processamento de Movers and Shakers")
    base_url_movers_shakers = "https://www.amazon.nl/gp/movers-and-shakers/"
    movers_shakers_products = process_category(base_url_movers_shakers, "movers_and_shakers")
    all_products.extend(movers_shakers_products)
    logging.info(f"Produtos de Movers and Shakers: {len(movers_shakers_products)}")

    # Pausa com intervalo aleatório para evitar sobrecarga no servidor
    time.sleep(random.uniform(5, 10))

    # Processa New Releases e adiciona à lista consolidada
    logging.info("Iniciando processamento de New Releases")
    base_url_new_releases = "https://www.amazon.nl/gp/new-releases/"
    new_releases_products = process_category(base_url_new_releases, "new_releases")
    all_products.extend(new_releases_products)
    logging.info(f"Produtos de New Releases: {len(new_releases_products)}")

    # Verifica se foram encontrados produtos
    if not all_products:
        logging.error("Nenhum produto encontrado para as categorias processadas.")
        print("Nenhum produto encontrado.")
        return

    # Cria um DataFrame com todos os produtos
    df_consolidated = pd.DataFrame(all_products)
    
    # Limpeza e formatação de reviews
    df_consolidated['reviews'] = df_consolidated['reviews'].apply(lambda x: re.sub(r'[.,]', '', str(x)))
    df_consolidated['reviews'] = df_consolidated['reviews'].replace("No reviews", 0)  # Substituir "No reviews" por 0
    df_consolidated['reviews'] = df_consolidated['reviews'].astype(int)

    # Salva todos os dados consolidados em um arquivo Excel único
    save_to_excel_consolidated(all_products, directory_path)

    logging.info("Processo finalizado!")  # Registra a finalização do processo
    logging.info((f"Produtos Totais encontrados: {len(best_sellers_products)}+{len(movers_shakers_products)}+{len(new_releases_products)}/ Total: 2600"))
    print("Base excel bruta salva")
    print((f"Produtos Totais encontrados: {len(best_sellers_products)}+{len(movers_shakers_products)}+{len(new_releases_products)}/ Total: 2600"))

    return df_consolidated

#if __name__ == "__main__":
    #extract_data()
    #print("Finalizado")