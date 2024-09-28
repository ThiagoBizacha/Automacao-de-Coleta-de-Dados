import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import time
from wordcloud import WordCloud
from app.components.data_loader import get_data
from app.components.filters import apply_filters
from app.components.kpi_calculator import calculate_kpis
from app.components.kpi_calculator import produto_top_5_frequente
from app.components.visualizations import render_pareto_chart

# Cache para carregar dados
@st.cache_data
def load_data():
    return get_data()
#--------------------------------------------------------------------------------------------------------------------------------
def show_page():
    
    # Título da página com data
    #def render_title_with_date(selected_date_range):
        #st.markdown(f"""
            #<div class="title-container">
                #<div class="title-left">DADOS AMAZON.NL - BEST SELLERS</div>
                #<div class="separator"></div>
                #<div class="subtitle">Data Selecionada: {selected_date_range[0]} até {selected_date_range[1]}</div>
            #</div>
        #""", unsafe_allow_html=True)
#--------------------------------------------------------------------------------------------------------------------------------
    # Carregar os dados com indicador visual de carregamento
    with st.spinner('Carregando dados...'):
        df = load_data()

#--------------------------------------------------------------------------------------------------------------------------------
# Filtros interativos
#--------------------------------------------------------------------------------------------------------------------------------

    st.sidebar.title("Filtros")

    min_date = df['date'].min().date()
    max_date = df['date'].max().date()

    date_range = st.sidebar.date_input("Selecione o intervalo de datas", [max_date, max_date], 
                                       min_value=min_date, max_value=max_date, key="best_sellers_date")  
  
    selected_categories = st.sidebar.multiselect("Selecione a(s) categoria(s)", ['Todas as Categorias'] + list(df['category'].unique()), key="best_sellers_category")
    
    keyword = st.sidebar.text_input("Digite uma palavra-chave no nome do produto", key="best_sellers_keyword")

    min_value, max_value = st.sidebar.slider("Selecione o intervalo de valor EUR", 
                                             float(df['value'].min()), float(df['value'].max()), 
                                             (float(df['value'].min()), float(df['value'].max())), key="best_sellers_value")

    # Aplicar filtros
    df_filtered = apply_filters(df, date_range, min_value, max_value, selected_categories, keyword)

    # Aplicar filtro de 'origin'
    df_filtered = df_filtered[df_filtered['origin'] == 'best_sellers']

    selected_date_range = [max_date, max_date]  # Substitua com as datas reais dos filtros
    #render_title_with_date(selected_date_range)

#--------------------------------------------------------------------------------------------------------------------------------

    # Cálculo de KPIs com cache
    @st.cache_data
    def load_kpis(filtered_data):
        return calculate_kpis(filtered_data)

    kpis = calculate_kpis(df_filtered)

    # Calcular o novo KPI produto mais frequente no Top 3
    produto_frequente, percentual_top_3 = produto_top_5_frequente(df)

    # Função para limitar o número de caracteres em um nome
    def limitar_caracteres(texto, max_chars=30):
        return texto if len(texto) <= max_chars else texto[:max_chars] + '...'
    
#--------------------------------------------------------------------------------------------------------------------------------
        # Exibição do card com a data atual selecionada e o total de produtos
#--------------------------------------------------------------------------------------------------------------------------------    

    # Data selecionada e total de produtos na base filtrada
    data_selecionada = selected_date_range[1]  # Data final do intervalo
    total_produtos = f"{len(df):,.0f}".replace(",", ".")

    # Exibir o card com a data selecionada e o total de produtos
    st.markdown(f"""
    <div class="kpi-box">
        <div style="display: inline-block; font-weight: bold; margin-right: 10px;">Total de produtos extraídos:</div>
        <div style="display: inline-block;">{total_produtos}</div>
    </div>
    """, unsafe_allow_html=True)

    # Pular uma linha entre os blocos
    st.markdown("<br>", unsafe_allow_html=True)

#--------------------------------------------------------------------------------------------------------------------------------
    # Exibição dos KPIs em três colunas
#--------------------------------------------------------------------------------------------------------------------------------    

    col1, col2, col3 = st.columns(3)

    # Coluna 1: Categoria com a maior média de score
    with col1:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Categoria mais recomendada</div>
            <div class="kpi-value">{kpis['categoria_maior_score']}</div>
            <div class="kpi-delta">Score comparado com todas as categorias: ↑ {kpis['comparacao_score']:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Coluna 2: Produto mais frequente no Top 3 com link
    with col2:
        nome_produto_top3 = limitar_caracteres(produto_frequente, max_chars=20)
        link_produto_top3 = df[df['name'] == produto_frequente]['link'].values[0]
        
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Produto mais frequente no Top 5</div>
            <div class="kpi-value">
                <a href="{link_produto_top3}" target="_blank" style="text-decoration: none; color: inherit;">
                    {nome_produto_top3}
                </a>
            </div>
            <div class="kpi-delta">Percentual de vezes no Top 5: {percentual_top_3:.2f}% do total</div>
        </div>
        """, unsafe_allow_html=True)

    # Coluna 3: Produto com maior crescimento de reviews com link
    with col3:
        nome_produto_reviews = limitar_caracteres(kpis['produto_crescimento_reviews'], max_chars=20)
        link_produto_reviews = df_filtered[df_filtered['name'] == kpis['produto_crescimento_reviews']]['link'].values[0]
        
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Produto com maior cresc. de reviews</div>
            <div class="kpi-value">
                <a href="{link_produto_reviews}" target="_blank" style="text-decoration: none; color: inherit;">
                    {nome_produto_reviews}
                </a>
            </div>
            <div class="kpi-delta">Aumento de reviews: ↑ {kpis['comparacao_reviews']:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

#--------------------------------------------------------------------------------------------------------------------------------
# Título da seção: Top 3 Categorias com Média de Score Mais Alta
#--------------------------------------------------------------------------------------------------------------------------------  
#   
    st.markdown("<div class='section-title'>Top 3 Categorias</div>", unsafe_allow_html=True)

    # Agrupando as 3 categorias com maior média de score
    top_3_categories = df_filtered.groupby('category')['score'].quantile(0.75).nlargest(3).reset_index()

    # Criar três colunas para os três indicadores
    col1, col2, col3 = st.columns(3)  # Divide em três colunas para exibir na horizontal

    # Exibir os resultados em cada coluna
    for i, row in enumerate(top_3_categories.iterrows()):
        # Usar a medalha de ouro para o primeiro lugar e as outras medalhas para os demais
        icon = "🥇" if i == 0 else ("🥈" if i == 1 else "🥉")

        col = [col1, col2, col3][i]  # Seleciona a coluna correspondente

        # Exibir o conteúdo na coluna
        with col:
            st.markdown(f"""
            <div class='kpi-box'>
                <div class='highlight-box'>
                    <div class='sub-indicator-title'>{icon} {row[1]['category']}</div>
                    <div class='highlight-value'>Score: {row[1]['score']:.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
#--------------------------------------------------------------------------------------------------------------------------------
# TOP 3 PRODUTOS POR RANK DAS TOP CATEGORIAS (DIVIDIR EM 3 COLUNAS)
#--------------------------------------------------------------------------------------------------------------------------------

    st.markdown("<div class='section-title'>Rank - Produtos por categoria</div>", unsafe_allow_html=True)

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
                    <div class='highlight-title'>
                        <a href="{product[1]['link']}" target="_blank" style="text-decoration: none; color: inherit;">
                            {product[1]['name']}
                        </a>
                    </div>
                    <div class='highlight-value'>€{product[1]['value']:.2f}</div>
                    <div class='highlight-details'>Reviews: {product[1]['reviews']}</div>
                    <div class='highlight-details'>Score: {product[1]['score']}</div>
                    <div class='highlight-details'>Rating: {product[1]['rating']}</div>
                </div>
                """, unsafe_allow_html=True)

#--------------------------------------------------------------------------------------------------------------------------------
 # TOP 3 PRODUTOS POR SCORE NO TOTAL DA BASE (EM LINHA)
 #--------------------------------------------------------------------------------------------------------------------------------

    st.markdown("<div class='section-title'>Top 3 Produtos por Score</div>", unsafe_allow_html=True)
    top_3_products_by_score = df_filtered.nlargest(3, 'score')

    col1, col2, col3 = st.columns(3)
    for idx, product in enumerate(top_3_products_by_score.iterrows()):
        col = [col1, col2, col3][idx]  # Seleciona a coluna correspondente
        with col:
            st.markdown(f"""
            <div class='highlight-box'>
                <img src="{product[1]['image']}" class='highlight-img'/>
                <div class='highlight-title'>
                        <a href="{product[1]['link']}" target="_blank" style="text-decoration: none; color: inherit;">
                            {product[1]['name']}
                        </a>                
                <div class='highlight-value'>€{product[1]['value']:.2f}</div>
                <div class='highlight-details'>Reviews: {product[1]['reviews']}</div>
                <div class='highlight-details'>Score: {product[1]['score']}</div>
                <div class='highlight-details'>Rating: {product[1]['rating']}</div>
                <div class='highlight-details'>Categoria: {product[1]['category']}</div>
            </div>
            """, unsafe_allow_html=True)

#--------------------------------------------------------------------------------------------------------------------------------
# TOP 3 PRODUTOS MAIS POPULARES (MAIS REVIEWS) (EM LINHA)
#--------------------------------------------------------------------------------------------------------------------------------

    st.markdown("<div class='section-title'>Top 3 Produtos mais populares (reviews)</div>", unsafe_allow_html=True)
    top_3_products_by_reviews = df_filtered.nlargest(3, 'reviews')

    col1, col2, col3 = st.columns(3)
    for idx, product in enumerate(top_3_products_by_reviews.iterrows()):
        col = [col1, col2, col3][idx]  # Seleciona a coluna correspondente
        with col:
            st.markdown(f"""
            <div class='highlight-box'>
                <img src="{product[1]['image']}" class='highlight-img'/>
                <div class='highlight-title'>
                        <a href="{product[1]['link']}" target="_blank" style="text-decoration: none; color: inherit;">
                            {product[1]['name']}
                        </a>
                    </div>               
                <div class='highlight-value'>€{product[1]['value']:.2f}</div>
                <div class='highlight-details'>Reviews: {product[1]['reviews']}</div>
                <div class='highlight-details'>Rating: {product[1]['rating']}</div>
                <div class='highlight-details'>Categoria: {product[1]['category']}</div>
            </div>
            """, unsafe_allow_html=True)

#--------------------------------------------------------------------------------------------------------------------------------
    # Nuvem de palavras
    st.subheader("PALAVRAS MAIS FREQUENTES")
    text = " ".join(name for name in df_filtered['name'])
    wordcloud = WordCloud(background_color="white", colormap="Blues", width=600, height=200).generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

#--------------------------------------------------------------------------------------------------------------------------------
    # Gráfico de Pareto
    st.subheader("PARETO POR CATEGORIA")
    render_pareto_chart(df_filtered)
#--------------------------------------------------------------------------------------------------------------------------------
    # Gráfico de dispersão
    if 'value' in df_filtered.columns and 'reviews' in df_filtered.columns and 'category' in df_filtered.columns:
        df_filtered = df_filtered.dropna(subset=['value', 'reviews', 'category'])

        if not df_filtered.empty:
            st.subheader("PRODUTOS - VALOR X REVIEW")
            scatter_chart = px.scatter(df_filtered, x='value', y='reviews', color='category', 
                                       hover_data=['name', 'value', 'reviews'], template='plotly_white'
                                       )
            st.plotly_chart(scatter_chart, use_container_width=True)
        else:
            st.write("Não há dados suficientes para gerar o gráfico de dispersão.")
    else:
        st.write("As colunas necessárias para gerar o gráfico não estão disponíveis.")

#--------------------------------------------------------------------------------------------------------------------------------
    # Tabela de produtos populares com ordenação
    st.subheader("PRODUTOS POR SCORE")
    top_produtos_score = df_filtered.nlargest(10, 'score')
    st.dataframe(top_produtos_score[['name', 'category', 'value', 'reviews', 'score', 'rating']].sort_values(by='score', ascending=False))
#--------------------------------------------------------------------------------------------------------------------------------   
    # Função para exibir o Top 3 por Rank em cada categoria
#--------------------------------------------------------------------------------------------------------------------------------
    def top_3_by_rank_per_category(df):
        # Filtrar para pegar os 3 produtos com menor rank em cada categoria
        top_3_rank_per_category = df.groupby('category').apply(lambda x: x.nsmallest(3, 'rank')).reset_index(drop=True)
        
        # Exibir a tabela
        st.subheader("TOP 3 PRODUTOS POR CATEGORIA")
        st.dataframe(top_3_rank_per_category[['category', 'name', 'rank', 'score', 'reviews', 'value']])

    # Exibir Top 3 por rank em cada categoria
    top_3_by_rank_per_category(df_filtered)
#--------------------------------------------------------------------------------------------------------------------------------
    # Tabela de produtos completos
#--------------------------------------------------------------------------------------------------------------------------------
    st.subheader("BASE COMPLETA")
    st.dataframe(df[['category', 'rank', 'asin', 'name', 'title', 'currency', 
                              'value', 'reviews', 'rating', 'score', 'link',
                              'date' , 'origin']].sort_values(by='score', ascending=False))
 #--------------------------------------------------------------------------------------------------------------------------------   






