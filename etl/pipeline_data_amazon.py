import extract_data_amazon  # Importa o módulo de extração
import transform_data_amazon  # Importa o módulo de transformação
import load_data_amazon  # Importa o módulo de carga
import load_postgresql  # Seu script de carga SQL
import time  # Importa a biblioteca time para medir o tempo de execução

def main_pipeline():
    """    
    Pipeline principal que coordena a extração, transformação e carga dos dados.
    """
    print("Pipeline iniciado")
    
    # Captura o tempo de início do pipeline
    start_time = time.time()

    # Extração: O DataFrame extraído de 'extract_data_amazon.py'
    df_consolidated = extract_data_amazon.extract_data()
    print("Extração finalizada")

    # Transformação: O DataFrame consolidado é passado para a função de transformação
    df_transformed = transform_data_amazon.transform_data(df_consolidated)
    print("Transformação finalizada")

    # Carga: O DataFrame limpo é passado para a função de carga para ser salvo
    load_data_amazon.load_data(df_transformed)

    # Carga dos dados no banco de dados PostgreSQL
    load_postgresql.load_to_postgresql(df_transformed)
    print("Carga SQL finalizada")

    # Captura o tempo de término do pipeline
    end_time = time.time()
    
    # Calcula o tempo total em minutos
    total_time_minutes = (end_time - start_time) / 60
    print(f"Pipeline finalizado! Tempo total: {total_time_minutes:.2f} minutos.")

if __name__ == "__main__":
    main_pipeline()
