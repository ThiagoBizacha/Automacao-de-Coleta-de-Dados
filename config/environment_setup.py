import os

def get_environment_settings():
    # Definir o ambiente (dev, test, prod) via variável de ambiente
    environment = os.getenv('ENV', 'development')  # O padrão será 'development'

    if environment == 'development':
        print("Executando em ambiente de Desenvolvimento")
        # Configurações específicas para dev
        return 'development'
    elif environment == 'testing':
        print("Executando em ambiente de Teste")
        # Configurações específicas para testes
        return 'testing'
    elif environment == 'production':
        print("Executando em ambiente de Produção")
        # Configurações específicas para produção
        return 'production'
    else:
        print(f"Ambiente desconhecido: {environment}")
        return None
