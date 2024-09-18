import pandas as pd

def calculate_kpis(df):
    if df.empty:
        return {
            'categoria_maior_score': 'Nenhum dado',
            'maior_valor_categoria': 'Nenhum dado',
            'produto_maior_reviews': 'Nenhum dado',
            'produto_maior_score': 'Nenhum dado',
            'comparacao_score': 0,
            'valor_total_categoria': 0,
            'total_produtos': 0 
        }

    try:
        # KPIs com segurança
        categoria_maior_score = df.groupby('category')['score'].mean().idxmax()
        maior_valor_categoria = df.groupby('category')['value'].sum().idxmax()
        produto_maior_reviews = df[df['reviews'] == df['reviews'].max()]['name'].values[0]
        produto_maior_score = df[df['score'] == df['score'].max()]['name'].values[0]

        # Calculando a média geral de score e a média da categoria com maior score
        media_score_geral = df['score'].mean()
        maior_score_categoria_media = df.groupby('category')['score'].mean().max()
        comparacao_score = ((maior_score_categoria_media - media_score_geral) / media_score_geral) * 100

        # Total de valor da categoria com maior valor
        valor_total_categoria = df.groupby('category')['value'].sum().max()

        total_produtos = len(df)

        return {
            'categoria_maior_score': categoria_maior_score,
            'maior_valor_categoria': maior_valor_categoria,
            'produto_maior_reviews': produto_maior_reviews,
            'produto_maior_score': produto_maior_score,
            'comparacao_score': comparacao_score,
            'valor_total_categoria': valor_total_categoria,
            'total_produtos': total_produtos
        }

    except Exception as e:
        # Em caso de erro, retornar 'Erro' em todos os KPIs
        return {
            'categoria_maior_score': 'Erro',
            'maior_valor_categoria': 'Erro',
            'produto_maior_reviews': 'Erro',
            'produto_maior_score': 'Erro',
            'comparacao_score': 0,
            'valor_total_categoria': 0,
            'total_produtos': 0
        }

