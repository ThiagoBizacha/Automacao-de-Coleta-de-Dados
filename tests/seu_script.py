import random

def execute():
    # Gera uma lista de 10 números aleatórios entre 1 e 100
    random_numbers = [random.randint(1, 100) for _ in range(10)]
    return f"Números gerados: {random_numbers}"
