# kpi_calculator.py
def calculate_kpis(df_filtered):
    """
    Calcula os KPIs com base nos dados filtrados.
    """
    categoria_maior_score = df_filtered.groupby('category')['score'].mean().idxmax()
    media_score_geral = df_filtered['score'].mean()
    maior_score_categoria_media = df_filtered.groupby('category')['score'].mean().max()
    comparacao_score = ((maior_score_categoria_media - media_score_geral) / media_score_geral) * 100

    maior_valor_categoria = df_filtered.groupby('category')['value'].sum().idxmax()
    valor_total_categoria = df_filtered.groupby('category')['value'].sum().max()

    produto_maior_reviews = df_filtered[df_filtered['reviews'] == df_filtered['reviews'].max()]['name'].values[0]
    produto_maior_score = df_filtered[df_filtered['score'] == df_filtered['score'].max()]['name'].values[0]

    return {
        "categoria_maior_score": categoria_maior_score,
        "comparacao_score": comparacao_score,
        "maior_valor_categoria": maior_valor_categoria,
        "valor_total_categoria": valor_total_categoria,
        "produto_maior_reviews": produto_maior_reviews,
        "produto_maior_score": produto_maior_score
    }
