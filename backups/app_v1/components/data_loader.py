# data_loader.py
import psycopg2
import pandas as pd

def get_data():
    """
    Conecta ao banco de dados PostgreSQL e retorna o DataFrame com os dados da Amazon.
    """
    conn = psycopg2.connect(
        host="localhost",
        database="proj_dropshipping",
        user="postgres",
        password="admin"
    )
    query = "SELECT * FROM public.amazon_nl_final;"
    df = pd.read_sql(query, conn)
    conn.close()

    # Garantir que a coluna 'date' esteja no formato datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    return df
