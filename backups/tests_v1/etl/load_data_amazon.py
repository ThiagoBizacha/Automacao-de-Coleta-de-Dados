import pandas as pd
import logging
from datetime import datetime

# Configuração do logging
logging.basicConfig(
    filename="C:/Users/ThiagoBizacha/Desktop/Projeto_Automacao_Coleta_Dados/logs/load_data.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

directory_path = "C:/Users/ThiagoBizacha/Desktop/Projeto_Automacao_Coleta_Dados/data/output/bot_amazon"

def load_data(df_transformed):
    """
    Simula a carga dos dados tratados, salvando-os em um arquivo CSV.
    
    Parâmetros:
        df_cleaned (DataFrame): DataFrame com os dados limpos e tratados.
    """
    try:
       
        # Define o nome do arquivo com base na data atual
        today_date = datetime.today().strftime('%Y-%m-%d')
        filename = f"{directory_path}/base_amazon_final_{today_date}.xlsx"
        
        # Salva o DataFrame em um arquivo Excel
        df_transformed.to_excel(filename, index=False)
        
        print("Carga excel final finalizada")
        logging.info(f"Dados carregados e salvos em {filename}.")
    except Exception as e:
        logging.error(f"Erro ao carregar os dados: {e}")

