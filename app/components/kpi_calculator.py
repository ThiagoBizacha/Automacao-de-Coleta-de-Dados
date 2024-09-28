def produto_top_5_frequente(df):
    if df.empty or 'rank' not in df.columns or 'date' not in df.columns or 'asin' not in df.columns:
        return 'Nenhum dado', 0

    # Filtrar produtos com rank <= 5 (Top 5)
    top_5_df = df[df['rank'] <= 5]

    if top_5_df.empty:
        return 'Nenhum dado', 0

    # Contar quantas vezes cada "asin" apareceu no Top 3 durante o período
    asin_frequencia = top_5_df.groupby('asin')['date'].nunique()

    # Encontrar o asin mais frequente
    asin_mais_frequente = asin_frequencia.idxmax()
    vezes_entre_top_3 = asin_frequencia.max()

    # Encontrar o nome correspondente ao asin mais frequente
    produto_frequente = df[df['asin'] == asin_mais_frequente]['name'].values[0]

    # Calcular o percentual de vezes no Top 3
    total_dias_analisados = df['date'].nunique()
    percentual_top_3 = (vezes_entre_top_3 / total_dias_analisados) * 100

    return produto_frequente, percentual_top_3


def calculate_kpis(df):
    kpis = {
        'categoria_maior_score': 'Nenhum dado',
        'maior_valor_categoria': 'Nenhum dado',
        'produto_maior_reviews': 'Nenhum dado',
        'produto_maior_score': 'Nenhum dado',
        'comparacao_score': 0,
        'valor_total_categoria': 0,
        'total_produtos': 0,
        'categoria_crescimento_score': 'Nenhum dado',
        'produto_top_5_frequente': 'Nenhum dado',
        'produto_crescimento_reviews': 'Nenhum dado',
        'comparacao_reviews': 0,
        'top_5_score': 0
    }

    if df.empty:
        return kpis

    try:
        # KPIs existentes
        kpis['categoria_maior_score'] = df.groupby('category')['score'].mean().idxmax()
        kpis['maior_valor_categoria'] = df.groupby('category')['value'].sum().idxmax()
        kpis['produto_maior_reviews'] = df[df['reviews'] == df['reviews'].max()]['name'].values[0]
        kpis['produto_maior_score'] = df[df['score'] == df['score'].max()]['name'].values[0]
        kpis['total_produtos'] = len(df)  # Correção no total de produtos

        # Comparação de score
        media_score_geral = df['score'].mean()
        maior_score_categoria_media = df.groupby('category')['score'].mean().max()
        kpis['comparacao_score'] = ((maior_score_categoria_media - media_score_geral) / media_score_geral) * 100

        # Valor total da categoria com maior valor
        kpis['valor_total_categoria'] = df.groupby('category')['value'].sum().max()

        # Produto mais frequente no Top 5
        if 'rank' in df.columns:
            top_5_df = df[df['rank'] <= 5]
            if not top_5_df.empty:
                kpis['produto_top_5_frequente'] = top_5_df['name'].value_counts().idxmax()
                total_top_5 = len(top_5_df)
                total_produtos = len(df)
                kpis['top_5_score'] = (total_top_5 / total_produtos) * 100

        # Produto com maior crescimento de reviews
        if 'reviews' in df.columns:
            kpis['produto_crescimento_reviews'] = df.loc[df['reviews'].diff().idxmax(), 'name']
            max_reviews = df['reviews'].max()
            kpis['comparacao_reviews'] = ((max_reviews - df['reviews'].mean()) / df['reviews'].mean()) * 100

        return kpis

    except Exception as e:
        print(f"Erro ao calcular KPIs: {e}")
        return kpis
