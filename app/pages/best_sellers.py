import streamlit as st
from app.components.data_loader import get_data
from app.components.filters import apply_filters
from app.components.kpi_calculator import calculate_kpis
from app.components.visualizations import render_pareto_chart
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import os

# Cache para carregar dados
@st.cache_data
def load_data():
    return get_data()

def show_page():
# Título com foco em boas práticas de design para páginas web
    def render_title_with_date(selected_date_range):
        st.markdown(f"""
            <style>
            /* Animação suave */
            @keyframes fadeIn {{
                0% {{ opacity: 0; transform: translateY(-10px); }}
                100% {{ opacity: 1; transform: translateY(0); }}
            }}

            /* Contêiner do título */
            .title-container {{
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                margin-bottom: 30px;
                padding: 10px 0;
                border-bottom: 2px solid #E0E0E0;
                animation: fadeIn 1.5s ease-in-out;
            }}

            /* Título principal */
            .title-left {{
                font-size: 58px;
                font-weight: 700;
                color: #34495E; /* Cor mais viva */
                margin: 0;
                padding: 0;
            }}

            /* Linha separadora */
            .separator {{
                width: 100px;
                height: 4px;
                background-color: #3498DB;
                border-radius: 2px;
                margin-top: 8px;
            }}

            /* Subtítulo com data */
            .subtitle {{
                font-size: 18px;
                color: #7D7D7D;
                font-weight: 400;
                margin-top: 8px;
            }}
            
            /* Animação de hover para o título */
            .title-left:hover {{
                color: #2980B9;
                transform: scale(1.05);
            }}
            </style>

            <div class="title-container">
                <div class="title-left">DADOS AMAZON.NL - BEST SELLERS</div>
                <div class="separator"></div>
                <div class="subtitle">Data Selecionada: {selected_date_range[0]} até {selected_date_range[1]}</div>
            </div>
        """, unsafe_allow_html=True)

    # CSS para melhorar os KPIs com fundo preto, tamanhos uniformes e estilo profissional
    st.markdown("""
        <style>
        /* Estilos de Contêiner dos KPIs */
        .kpi-container {
            background-color: #202020;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            color: #FFFFFF;
            width: 100%;  
            min-height: 150px;  
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .kpi-container:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 16px rgba(255, 255, 255, 0.1);
        }

        /* Estilos do Título e Valores */
        .kpi-title {
            font-size: 20px;
            font-weight: 500;
            margin-bottom: 10px;
            color: #BBBBBB;
        }
        .kpi-value {
            font-size: 40px;
            font-weight: bold;
            color: #00FFAA;
        }
        .kpi-delta {
            font-size: 16px;
            color: #FF5733;
        }

        /* Layout Responsivo */
        .kpi-row {
            display: flex;
            justify-content: space-between;
            gap: 20px;
            margin-bottom: 20px;
        }
        .kpi-column {
            flex: 1;
        }

        /* Responsividade */
        @media (max-width: 768px) {
            .kpi-row {
                flex-direction: column;
            }
        }
        </style>
    """, unsafe_allow_html=True)

      # CSS para personalização dos indicadores
    st.markdown("""
        <style>
        /* CSS dos indicadores */
        .highlight-box {
            #background-color: #202020;
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
            color: white;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .highlight-box:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 16px rgba(255, 255, 255, 0.1);
        }
        .highlight-title {
            font-size: 20px;
            font-weight: bold;
            color: #00FFAA;
        }
        .highlight-value {
            font-size: 20px;
            font-weight: bold;
            color: #FFFFFF;
        }
        .highlight-details {
            font-size: 18px;
            color: #AAAAAA;
            margin-top: 5px;
        }
        .highlight-img {
            margin-top: 10px;
            border-radius: 10px;
            width: 280px;
        }
        /* Layout responsivo para organizar os indicadores */
        .kpi-row {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 20px;
        }
        .kpi-box {
            flex: 1;
            min-width: 250px;
            max-width: 300px;
        }
        /* Responsividade */
        @media (max-width: 768px) {
            .kpi-row {
                flex-direction: column;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # Carregar os dados com indicador visual de carregamento
    with st.spinner('Carregando dados...'):
        df = load_data()

    # Filtros interativos
    st.sidebar.title("Filtros Interativos")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()

    date_range = st.sidebar.date_input("Selecione o intervalo de datas", [max_date, max_date], 
                                       min_value=min_date, max_value=max_date, key="best_sellers_date")
    
    min_value, max_value = st.sidebar.slider("Selecione o intervalo de valor (value)", 
                                             float(df['value'].min()), float(df['value'].max()), 
                                             (float(df['value'].min()), float(df['value'].max())), key="best_sellers_value")
    
    selected_categories = st.sidebar.multiselect("Selecione a(s) categoria(s)", ['Todas as Categorias'] + list(df['category'].unique()), key="best_sellers_category")
    
    keyword = st.sidebar.text_input("Digite uma palavra-chave no nome do produto", key="best_sellers_keyword")

    # Aplicar filtros
    df_filtered = apply_filters(df, date_range, min_value, max_value, selected_categories, keyword)

    # Aplicar filtro de 'origin'
    df_filtered = df_filtered[df_filtered['origin'] == 'best_sellers']

    selected_date_range = [max_date, max_date]  # Substitua com as datas reais dos filtros
    render_title_with_date(selected_date_range)

    # Cálculo de KPIs com cache
    @st.cache_data
    def load_kpis(filtered_data):
        return calculate_kpis(filtered_data)

    kpis = load_kpis(df_filtered)

    # Exibição dos KPIs
    st.markdown('<div class="kpi-row">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Categoria com a maior média de score</div>
            <div class="kpi-value">{kpis['categoria_maior_score']}</div>
            <div class="kpi-delta">↑ {kpis['comparacao_score']:.2f}% acima da média geral</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Categoria com o maior valor total</div>
            <div class="kpi-value">€ {kpis['valor_total_categoria']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Total de produtos no dia</div>
            <div class="kpi-value">{kpis['total_produtos']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Fechar a primeira linha de KPIs

    st.markdown('<div class="kpi-row">', unsafe_allow_html=True)
    
      # TOP 3 CATEGORIAS COM MÉDIA DE SCORE MAIS ALTA
    st.markdown("### Top 3 Categorias com Média de Score Mais Alta")
    top_3_categories = df_filtered.groupby('category')['score'].mean().nlargest(3).reset_index()

    st.markdown('<div class="kpi-row">', unsafe_allow_html=True)
    for i, row in top_3_categories.iterrows():
        icon = "🏆" if i == 0 else ("🥈" if i == 1 else "🥉")
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='highlight-box'>
                <div class='highlight-title'>{icon} {row['category']}</div>
                <div class='highlight-value'>Média de Score: {row['score']:.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # TOP 3 PRODUTOS POR RANK DAS TOP CATEGORIAS (DIVIDIR EM 3 COLUNAS)
    st.markdown("### Top 3 Produtos por Rank das Top Categorias")
    
    for i, row in top_3_categories.iterrows():
        category = row['category']
        st.markdown(f"#### {category}")
        top_3_ranked_products = df_filtered[df_filtered['category'] == category].nsmallest(3, 'rank')

        # Mostrar os produtos em 3 colunas
        col1, col2, col3 = st.columns(3)

        for idx, product in enumerate(top_3_ranked_products.iterrows()):
            col = [col1, col2, col3][idx]  # Seleciona a coluna correspondente
            with col:
                st.markdown(f"""
                <div class='highlight-box'> 
                    <div class='highlight-details'>Rank: {product[1]['rank']}</div>                   
                    <img src="{product[1]['image']}" class='highlight-img'/>
                    <div class='highlight-title'>{product[1]['name']}</div>
                    <div class='highlight-value'>€{product[1]['value']:.2f}</div>
                    <div class='highlight-details'>Reviews: {product[1]['reviews']}</div>
                    <div class='highlight-details'>Score: {product[1]['score']}</div>
                    <div class='highlight-details'>Rating: {product[1]['rating']}</div>
                </div>
                """, unsafe_allow_html=True)

    # TOP 3 PRODUTOS POR SCORE NO TOTAL DA BASE (EM LINHA)
    st.markdown("### Top 3 Produtos por Score no Total da Base")
    top_3_products_by_score = df_filtered.nlargest(3, 'score')

    col1, col2, col3 = st.columns(3)
    for idx, product in enumerate(top_3_products_by_score.iterrows()):
        col = [col1, col2, col3][idx]  # Seleciona a coluna correspondente
        with col:
            st.markdown(f"""
            <div class='highlight-box'>
                <img src="{product[1]['image']}" class='highlight-img'/>
                <div class='highlight-title'>{product[1]['name']}</div>                
                <div class='highlight-value'>€{product[1]['value']:.2f}</div>
                <div class='highlight-details'>Reviews: {product[1]['reviews']}</div>
                <div class='highlight-details'>Score: {product[1]['score']}</div>
                <div class='highlight-details'>Rating: {product[1]['rating']}</div>
            </div>
            """, unsafe_allow_html=True)

    # TOP 3 PRODUTOS MAIS POPULARES (MAIS REVIEWS) (EM LINHA)
    st.markdown("### Top 3 Produtos Mais Populares (Mais Reviews)")
    top_3_products_by_reviews = df_filtered.nlargest(3, 'reviews')

    col1, col2, col3 = st.columns(3)
    for idx, product in enumerate(top_3_products_by_reviews.iterrows()):
        col = [col1, col2, col3][idx]  # Seleciona a coluna correspondente
        with col:
            st.markdown(f"""
            <div class='highlight-box'>
                <img src="{product[1]['image']}" class='highlight-img'/>
                <div class='highlight-title'>{product[1]['name']}</div>                
                <div class='highlight-value'>€{product[1]['value']:.2f}</div>
                <div class='highlight-details'>Reviews: {product[1]['reviews']}</div>
                <div class='highlight-details'>Rating: {product[1]['rating']}</div>
            </div>
            """, unsafe_allow_html=True)

    # Gráfico de Pareto \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    render_pareto_chart(df_filtered)

    # Gráfico de dispersão
    if 'value' in df_filtered.columns and 'reviews' in df_filtered.columns and 'category' in df_filtered.columns:
        df_filtered = df_filtered.dropna(subset=['value', 'reviews', 'category'])

        if not df_filtered.empty:
            st.subheader("Dispersão por Produto - Valor x Reviews")
            scatter_chart = px.scatter(df_filtered, x='value', y='reviews', color='category', 
                                       hover_data=['name', 'value', 'reviews'], template='plotly_white', 
                                       title="Dispersão de Valor x Reviews")
            st.plotly_chart(scatter_chart, use_container_width=True)
        else:
            st.write("Não há dados suficientes para gerar o gráfico de dispersão.")
    else:
        st.write("As colunas necessárias para gerar o gráfico não estão disponíveis.")

    # Nuvem de palavras
    st.subheader("Nuvem de Palavras dos Produtos")
    text = " ".join(name for name in df_filtered['name'])
    wordcloud = WordCloud(background_color="white", colormap="Blues", width=800, height=400).generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

    # Tabela de produtos populares com ordenação
    st.subheader("Top Produtos por Score")
    top_produtos_score = df_filtered.nlargest(10, 'score')
    st.dataframe(top_produtos_score[['name', 'category', 'value', 'reviews', 'score', 'rating']].sort_values(by='score', ascending=False))
   
       # Função para exibir o Top 3 por Rank em cada categoria
    def top_3_by_rank_per_category(df):
        # Filtrar para pegar os 3 produtos com menor rank em cada categoria
        top_3_rank_per_category = df.groupby('category').apply(lambda x: x.nsmallest(3, 'rank')).reset_index(drop=True)
        
        # Exibir a tabela
        st.subheader("Top 3 Produtos por Rank em Cada Categoria")
        st.dataframe(top_3_rank_per_category[['category', 'name', 'rank', 'score', 'reviews', 'value']])

    # Exibir Top 3 por rank em cada categoria
    top_3_by_rank_per_category(df_filtered)

    # Total produtos

    # Tabela de produtos populares com ordenação
    st.subheader("BASE COMPLETA")
    st.dataframe(df[['category', 'rank', 'asin', 'name', 'title', 'currency', 
                              'value', 'reviews', 'rating', 'score', 'link',
                              'date' , 'origin']].sort_values(by='score', ascending=False))
       
