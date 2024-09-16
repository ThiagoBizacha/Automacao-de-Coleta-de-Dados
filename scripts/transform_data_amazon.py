import pandas as pd
import logging
import os

# Diretório para salvar os logs
log_directory = "C:/Users/ThiagoBizacha/Desktop/Projeto_Automacao_Coleta_Dados/logs/"
os.makedirs(log_directory, exist_ok=True)  # Cria o diretório de logs se ele ainda não existir

# Configuração do logging
logging.basicConfig(
    filename=os.path.join(log_directory, 'amazon_transform_data.log'),  # Define o nome e local do arquivo de log
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info(f"Tratamento iniciado")  

def clean_data(df):
    """Limpa e formata os dados extraídos da Amazon."""
    df['rank'] = df['rank'].str.replace('#', '', regex=False)

    df['rating'] = df['rating'].str.replace(' van 5 sterren', '').replace('No rating', "3").str.replace(",", ".").astype(float)

    df['reviews'] = df['reviews'].astype(str).str.replace('.', '', regex=False)  # Remove separadores de milhar
    df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce')  # Converte para numérico (coerce converte inválidos para NaN)
    df['reviews'] = df['reviews'].replace(0, 1)

    df['value'] = pd.to_numeric(df['value'].str.replace(',', '.'), errors='coerce').round(2)
    df['currency'] = df['symbol'].str.replace('€', 'EUR')
    
    # Filtramos e redefinimos o DataFrame, evitando cópias implícitas
    df = df[df['value'] <= 200]

    # Filtra o DataFrame removendo as categorias "Amazon Renewed" e "Amazon-apparaten & accessoires"
    df = df[~df['category'].isin(['Amazon Renewed', 'Amazon-apparaten & accessoires'])]

    logging.info('Dados limpos e valores inválidos removidos.')
    return df

def normalize_column(df, column):
    """Normaliza uma coluna usando min-max normalization."""
    return (df[column] - df[column].min()) / (df[column].max() - df[column].min())

def calculate_fields(df):
    """Adiciona campos normalizados e calcula o score e value_total."""
    df['normal_rating'] = normalize_column(df, 'rating')
    df['normal_reviews'] = normalize_column(df, 'reviews')
    df['normal_value'] = normalize_column(df, 'value')

    df['score'] = ((0.05 * df['normal_rating'] + 
                    0.7 * df['normal_reviews'] + 
                    0.25 * df['normal_value']) * 1000).astype(int)
    df['value_total'] = (df['value'] * df['reviews']).round(2)

    logging.info('Campos calculados adicionados com sucesso.')
    return df

def transform_data(df_consolidated):
    """
    Executa o pipeline de transformação no DataFrame extraído (df_consolidated).
    
    Parâmetros:
        df_consolidated (DataFrame): DataFrame consolidado da extração.
    
    Retorno:
        DataFrame: DataFrame limpo e com campos calculados.
    """
    print("Tratamento iniciado")
    df_cleaned = clean_data(df_consolidated)
    
    df_transformed = calculate_fields(df_cleaned)

    logging.info("Transformação finalizada.")
    #print("Transformação finalizada")
    return df_transformed

