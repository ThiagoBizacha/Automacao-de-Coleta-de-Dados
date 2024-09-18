import psycopg2

def load_to_postgresql(df):
    """Carrega os dados do DataFrame no banco de dados PostgreSQL."""
    conn = psycopg2.connect(
        host="localhost",
        database="proj_dropshipping",
        user="postgres",
        password="admin"
    )
    print("Conexão com o banco de dados realizada com sucesso!")

    cursor = conn.cursor()

    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO public.amazon_nl_final (
                category, rank, asin, name, title, rating, reviews, currency, value, image, link, date, origin,  
                normal_rating, normal_reviews, normal_value, score, value_total
            ) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
            row['category'], row['rank'], row['asin'], row['name'], row['title'], row['rating'], row['reviews'],
            row['currency'], row['value'], row['image'], row['link'], row['date'], row['origin'], row['normal_rating'], 
            row['normal_reviews'], row['normal_value'], row['score'], row['value_total']
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Dados carregados com sucesso no PostgreSQL.")
