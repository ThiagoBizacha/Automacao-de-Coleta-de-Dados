import pandas as pd
import logging
import os
import numpy as np

# Diretório para salvar os logs
log_directory = "C:/Users/ThiagoBizacha/Desktop/Projeto_Automacao_Coleta_Dados/data/logs/"
os.makedirs(log_directory, exist_ok=True)  # Cria o diretório de logs se ele ainda não existir

# Configuração do logging
logging.basicConfig(
    filename=os.path.join(log_directory, 'amazon_transform_data.log'),  # Define o nome e local do arquivo de log
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Tratamento iniciado")

def clean_data(df):
    """Limpa e formata os dados extraídos da Amazon."""
    try:
        # Tratamento da coluna 'rank'
        df['rank'] = df['rank'].str.replace('#', '', regex=False).astype(float)
        df['rank'] = df['rank'].fillna(0).astype(int)

        # Tratamento da coluna 'rating'
        df['rating'] = df['rating'].str.replace(' van 5 sterren', '').replace('No rating', "3").str.replace(",", ".")
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(3).round(2)

        # Tratamento da coluna 'reviews'
        df['reviews'] = df['reviews'].astype(str).str.replace('.', '', regex=False)  # Remove separadores de milhar
        df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce').fillna(1).astype(int)

        # Tratamento da coluna 'value'
        df['value'] = pd.to_numeric(df['value'].str.replace(',', '.'), errors='coerce').fillna(999999).round(2)

        # Remover linhas com valor maior que 200
        df = df[df['value'] <= 200]

        # Filtra o DataFrame removendo categorias indesejadas
        df = df[~df['category'].isin(['Amazon Renewed', 'Amazon-apparaten & accessoires', 'Cadeaubonnen', 'Kindle Store'])]

        # Adicionar a coluna de moeda
        df['symbol'] = df['symbol'].str.replace('€', 'EUR')
        df = df.rename(columns={'symbol': 'currency'})


        logging.info('Dados limpos e valores inválidos removidos.')
        return df
    
    except Exception as e:
        logging.error(f"Erro durante o processo de limpeza de dados: {e}")
        raise e

def normalize_column(df, column):
    """Normaliza uma coluna usando min-max normalization."""
    try:
        min_val = df[column].min()
        max_val = df[column].max()
        if max_val != min_val:
            return (df[column] - min_val) / (max_val - min_val)
        else:
            return np.zeros(df.shape[0])  # Retorna uma coluna de zeros se min == max
    
    except Exception as e:
        logging.error(f"Erro ao normalizar a coluna {column}: {e}")
        raise e

def calculate_fields(df):
    """Adiciona campos normalizados e calcula o score e value_total."""
    try:
        # Normaliza as colunas
        df['normal_rating'] = normalize_column(df, 'rating')
        df['normal_reviews'] = normalize_column(df, 'reviews')
        df['normal_value'] = normalize_column(df, 'value')

        # Para o rank, normalizamos e invertemos a escala (menor rank = melhor)
        df['normal_rank'] = 1 - normalize_column(df, 'rank') # Inverte a normalização

        # Cálculo do score, agora com rank inversamente proporcional
        df['score'] = ((0.05 * df['normal_rating'] + 
                        0.3 * df['normal_reviews'] + 
                        0.5 * df['normal_rank'] +  # Utilizamos o rank invertido
                        0.15 * df['normal_value']) * 1000).astype(int)

        # Cálculo do value_total
        df['value_total'] = (df['value'] * df['reviews']).round(2)

        logging.info('Campos calculados adicionados com sucesso.')
        return df
    
    except Exception as e:
        logging.error(f"Erro ao calcular os campos: {e}")
        raise e


def transform_data(df_consolidated):
    """
    Executa o pipeline de transformação no DataFrame extraído (df_consolidated).
    
    Parâmetros:
        df_consolidated (DataFrame): DataFrame consolidado da extração.
    
    Retorno:
        DataFrame: DataFrame limpo e com campos calculados.
    """
    logging.info("Iniciando transformação")
    
    try:
        df_cleaned = clean_data(df_consolidated)
        df_transformed = calculate_fields(df_cleaned)
        logging.info("Transformação finalizada.")
        return df_transformed
    
    except Exception as e:
        logging.error(f"Erro na transformação de dados: {e}")
        raise e

# Exemplo de aplicação
#df_transformed = transform_data(df)

# Analise descritiva

#print(df_transformed.describe())
#print(df_transformed.describe(include='all'))
#print(df_transformed['rank'].value_counts())
#print(df_transformed.isna().sum())


