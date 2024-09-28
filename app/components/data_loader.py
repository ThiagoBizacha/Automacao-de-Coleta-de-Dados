# data_loader.py
import psycopg2
import pandas as pd

def get_data():
    """
    Conecta ao banco de dados PostgreSQL e retorna o DataFrame com os dados da Amazon.
    """
    conn = psycopg2.connect(
        host="db-thiago-390438668051.cniie2kemucx.us-east-2.rds.amazonaws.com",
        database="postgres",
        user="postgres",
        password="M3GFMwk3BteZfZyJVz4Y"
    )
    query = "SELECT * FROM public.amazon_nl_final;"
    df = pd.read_sql(query, conn)
    conn.close()

    # Garantir que a coluna 'date' esteja no formato datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Filtrar as categorias indesejadas
    #df = df[~df['category'].isin(['Cadeaubonnen', 'Kindle Store'])]

    return df
