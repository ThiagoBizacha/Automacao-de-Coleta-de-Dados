from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter URL do banco de dados a partir das variáveis de ambiente
database_url = os.getenv('DATABASE_URL')

# Configurar conexão com o banco de dados usando SQLAlchemy
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

# Verificar a conexão
try:
    connection = engine.connect()
    print("Conexão com o banco de dados estabelecida com sucesso!")
    connection.close()
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
