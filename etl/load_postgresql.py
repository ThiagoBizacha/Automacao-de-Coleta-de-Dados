##### CARGA FINAL POSTGRESQL

import psycopg2
import logging 
import os
from dotenv import load_dotenv

# Caminho absoluto do arquivo .env baseado no diretório de trabalho atual
project_root = os.getcwd()
dotenv_path = os.path.join(project_root, 'config', '.env')

# Diretório para salvar os logs
log_directory = "C:/Users/ThiagoBizacha/Desktop/Projeto_Automacao_Coleta_Dados/data/logs/"
os.makedirs(log_directory, exist_ok=True)  # Cria o diretório de logs se ele ainda não existir

# Configuração do logging para salvar no diretório especificado
logging.basicConfig(
    filename=os.path.join(log_directory, 'amazon_load_sql.log'),  # Define o nome e local do arquivo de log
    level=logging.INFO,  # Define o nível de log (INFO), para registrar eventos gerais
    format='%(asctime)s - %(levelname)s - %(message)s'  # Define o formato da mensagem de log: data/hora, nível e mensagem
)

logging.info(f"Extração iniciada")  

def load_to_postgresql(df):
    """Carrega os dados do DataFrame no banco de dados PostgreSQL."""
    conn = psycopg2.connect(
        host="",
        database="postgres",
        user="postgres",
        password=""
    )
    logging.info(f"Conexão com o banco de dados realizada com sucesso!")  
    print("Conexão com o banco de dados realizada com sucesso!")

    cursor = conn.cursor()

    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO public.amazon_nl_final (
                category, rank, asin, name, title, rating, reviews, currency, value, image, link, date, origin,  
                normal_rating, normal_reviews, normal_value, score, value_total, normal_rank, classificacao_vendas, 
                classificacao_vendas_anterior, perc_alta
            ) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
            row['category'], row['rank'], row['asin'], row['name'], row['title'], row['rating'], row['reviews'],
            row['currency'], row['value'], row['image'], row['link'], row['date'], row['origin'], row['normal_rating'], 
            row['normal_reviews'], row['normal_value'], row['score'], row['value_total'], 
            row['normal_rank'], row['classificacao_vendas'], row['classificacao_vendas_anterior'], row['perc_alta']
        ))

    conn.commit()
    cursor.close()
    conn.close()
    logging.info(f"Dados carregados com sucesso no PostgreSQL - amazon_nl_final.") 
    print("Dados carregados com sucesso no PostgreSQL - amazon_nl_final.")

#//////////////////////// ##### CARGA BRUTA POSTGRESQL/////////////////////////////

def load_to_postgresql_bruto(df):
    """Carrega os dados do DataFrame no banco de dados PostgreSQL."""
    conn = psycopg2.connect(
        host="db-thiago-390438668051.cniie2kemucx.us-east-2.rds.amazonaws.com",
        database="postgres",
        user="postgres",
        password="M3GFMwk3BteZfZyJVz4Y"
    )
    logging.info(f"Conexão com o banco de dados realizada com sucesso!")  
    print("Conexão com o banco de dados realizada com sucesso!")

    cursor = conn.cursor()

    # Iterando sobre as linhas do DataFrame e inserindo os dados na tabela
    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO public.extract_amazon_full (
                category, rank, asin, name, title, rating, reviews, symbol, value, image, link, perc_alta, 
                classificacao_vendas, classificacao_vendas_anterior, date, origin
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
            row['category'], row['rank'], row['asin'], row['name'], row['title'], row['rating'], row['reviews'],
            row['symbol'], row['value'], row['image'], row['link'], row['perc_alta'], 
            row['classificacao_vendas'], row['classificacao_vendas_anterior'], row['date'], row['origin']
        ))

    # Confirmando as mudanças no banco de dados
    conn.commit()
    
    # Fechando a conexão com o banco de dados
    cursor.close()
    conn.close()
    
    print("Dados brutos carregados com sucesso no PostgreSQL - extract_amazon_full.")
