import streamlit as st
from app.components.data_loader import get_data
from app.components.filters import apply_filters
from app.components.kpi_calculator import calculate_kpis
from app.components.visualizations import render_pareto_chart
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

def show_page():

    st.title("DADOS AMAZON - NEW RELEASES")

    # Carregar os dados
    df = get_data()

    # Filtros interativos
    st.sidebar.title("Filtros Interativos")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    date_range = st.sidebar.date_input("Selecione o intervalo de datas", [max_date, max_date], min_value=min_date, max_value=max_date)


    min_value, max_value = st.sidebar.slider("Selecione o intervalo de valor (value)", 
                                             float(df['value'].min()), 
                                             float(df['value'].max()), 
                                             (float(df['value'].min()), float(df['value'].max())))

    selected_category = st.sidebar.selectbox("Selecione a categoria (category)", ['Todas as Categorias'] + list(df['category'].unique()))
    #selected_origin = st.sidebar.selectbox("Selecione a origem (origin)", ['Todos os Origens'] + list(df['origin'].unique()))
    keyword = st.sidebar.text_input("Digite uma palavra-chave no nome do produto")

    # Aplicar filtros
    df_filtered = apply_filters(df, date_range, min_value, max_value, selected_category, keyword)

    # Aplicar filtro de 'origin' ao DataFrame
    #if selected_origin != 'Todos os Origens':
    df_filtered = df_filtered[df_filtered['origin'] == 'new_releases']

    # KPIs
    kpis = calculate_kpis(df_filtered)
    st.metric("Categoria com a maior média de score", kpis['categoria_maior_score'], f"↑ {kpis['comparacao_score']:.2f}% acima da média geral")
    st.metric("Categoria com o maior valor total", kpis['maior_valor_categoria'], f"€ {kpis['valor_total_categoria']:.2f}")
    st.metric("Produto com maior número de reviews", kpis['produto_maior_reviews'])
    st.metric("Produto com o maior score", kpis['produto_maior_score'])
    st.metric('Total de produtos', kpis['total_produtos'])

    # Gráfico de Pareto
    render_pareto_chart(df_filtered)

    # Nuvem de palavras
    st.subheader("Nuvem de Palavras dos Produtos")
    text = " ".join(name for name in df_filtered['name'])
    wordcloud = WordCloud(background_color="white", colormap="Blues", width=800, height=400).generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

    # Tabela de produtos populares
    st.subheader("Top Produtos por Score Combinado")
    df_filtered['score_combinado'] = (df_filtered['score'] * 0.4) + (df_filtered['reviews'] * 0.3) + (1 / df_filtered['value'] * 0.3)
    top_produtos_score_combinado = df_filtered.nlargest(10, 'score_combinado')
    st.dataframe(top_produtos_score_combinado[['name', 'category', 'value', 'reviews', 'score', 'score_combinado']])
