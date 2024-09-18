import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from data_loader import get_data
from filters import apply_filters
from kpi_calculator import calculate_kpis
from visualizations import render_pareto_chart

# Configuração do layout da página
st.set_page_config(page_title="Análise Estratégica de Dados Amazon", layout="wide", page_icon="📊")

# CSS customizado para animações e estilos
st.markdown("""
    <style>
    .podium-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin-bottom: 40px;
    }
    .podium-item {
        text-align: center;
        transition: transform 0.3s ease;
    }
    .podium-item img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .podium-item img:hover {
        transform: scale(1.1);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    }
    .podium-item .medal {
        font-size: 36px;
        font-weight: bold;
        color: gold;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Carregar os dados
df = get_data()

# Filtros interativos
st.sidebar.title("Filtros Interativos")
min_date = df['date'].min().date()
max_date = df['date'].max().date()
date_range = st.sidebar.date_input("Selecione o intervalo de datas", [min_date, max_date])

min_value, max_value = st.sidebar.slider("Selecione o intervalo de valor (value)", 
                                         float(df['value'].min()), 
                                         float(df['value'].max()), 
                                         (float(df['value'].min()), float(df['value'].max())))

all_categories = ['Todas as Categorias'] + list(df['category'].unique())
selected_category = st.sidebar.selectbox("Selecione a categoria (category)", options=all_categories)

# Novo filtro para o campo 'origin'
all_origins = ['Todos os Origens'] + list(df['origin'].unique())  # Adiciona a opção de "Todos"
selected_origin = st.sidebar.selectbox("Selecione a origem (origin)", options=all_origins)

keyword = st.sidebar.text_input("Digite uma palavra-chave no nome do produto")

min_score, max_score = st.sidebar.slider("Selecione o intervalo de score", 
                                         float(df['score'].min()), 
                                         float(df['score'].max()), 
                                         (float(df['score'].min()), float(df['score'].max())))

# Aplicar filtros
df_filtered = apply_filters(df, date_range, min_value, max_value, selected_category, keyword, min_score, max_score)

# Aplicar filtro de 'origin' ao DataFrame
if selected_origin != 'Todos os Origens':
    df_filtered = df_filtered[df_filtered['origin'] == selected_origin]

# Criar score combinado para tomada de decisão
df_filtered['score_combinado'] = (df_filtered['score'] * 0.4) + (df_filtered['reviews'] * 0.3) + (1 / df_filtered['value'] * 0.3)

# Exibir KPIs
st.title("Análise Estratégica de Dados Amazon")
st.markdown("Esta página apresenta uma análise detalhada dos dados coletados da Amazon, com base em produtos, categorias, e performances diversas.")

kpis = calculate_kpis(df_filtered)
st.metric("Categoria com a maior média de score", kpis['categoria_maior_score'], f"↑ {kpis['comparacao_score']:.2f}% acima da média geral")
st.metric("Categoria com o maior valor total", kpis['maior_valor_categoria'], f"€ {kpis['valor_total_categoria']:.2f}")
st.metric("Produto com maior número de reviews", kpis['produto_maior_reviews'])
st.metric("Produto com o maior score", kpis['produto_maior_score'])

# Separar visualmente os KPIs
st.markdown("---")

# Análise 1: Produtos Populares com Boas Avaliações
st.subheader("Produtos Populares com Boas Avaliações")
produtos_populares = df_filtered[(df_filtered['reviews'] >= 100) & (df_filtered['score'] >= 4)]
st.write(f"Total de produtos populares: {len(produtos_populares)}")
st.dataframe(produtos_populares[['name', 'category', 'value', 'reviews', 'score']])

# Análise 2: Produtos com Margens Altas
st.subheader("Produtos com Potencial de Alta Margem de Lucro")
produtos_alta_margem = df_filtered[df_filtered['value'] < df_filtered['value'].mean()]
produtos_alta_margem = produtos_alta_margem.nlargest(10, 'score_combinado')
st.write(f"Total de produtos com alta margem de lucro: {len(produtos_alta_margem)}")
st.dataframe(produtos_alta_margem[['name', 'category', 'value', 'reviews', 'score', 'score_combinado']])

# Análise 3: Categorias Emergentes (baseado em avaliações recentes)
st.subheader("Categorias Emergentes com Base em Avaliações Recentes")
categoria_emergente = df_filtered.groupby('category')['reviews'].sum().reset_index().nlargest(5, 'reviews')
st.write("Top 5 Categorias Emergentes")
st.bar_chart(categoria_emergente.set_index('category'))

# Gráfico de Pareto para Score por Categoria
st.subheader("Gráfico de Pareto - Média de Score por Categoria")
render_pareto_chart(df_filtered)

# Verificar se as colunas necessárias estão no DataFrame antes de gerar o gráfico de dispersão
if 'value' in df_filtered.columns and 'reviews' in df_filtered.columns and 'category' in df_filtered.columns:
    df_filtered = df_filtered.dropna(subset=['value', 'reviews', 'category'])

    if not df_filtered.empty:
        st.subheader("Dispersão por Produto - Valor x Reviews")
        scatter_chart = px.scatter(df_filtered, x='value', y='reviews', color='category',
                                   hover_data=['name', 'value', 'reviews'], template='plotly_dark',
                                   title="Dispersão de Valor x Reviews")
        st.plotly_chart(scatter_chart, use_container_width=True)
    else:
        st.write("Não há dados suficientes para gerar o gráfico de dispersão.")
else:
    st.write("As colunas necessárias para gerar o gráfico não estão disponíveis.")

# Gráfico de Nuvem de Palavras
st.subheader("Nuvem de Palavras dos Produtos (coluna name)")
text = " ".join(name for name in df_filtered['name'])
wordcloud = WordCloud(background_color="white", colormap="Blues", width=800, height=400).generate(text)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# Top 3 Produtos com Imagens e Animações
st.subheader("Top 3 Produtos por Score")
top_3_produtos = df_filtered.nlargest(3, 'score')[['name', 'score', 'image', 'reviews']]

# Função para verificar se a imagem está disponível, caso contrário, usar uma imagem padrão
def get_image_url(row):
    if pd.notna(row['image']) and row['image'] != '':
        return row['image']
    else:
        return 'https://via.placeholder.com/150'  # URL da imagem padrão

# Layout dos 3 primeiros produtos
st.markdown('<div class="podium-container">', unsafe_allow_html=True)

# Primeiro lugar
st.markdown(f'''
    <div class="podium-item">
        <div class="medal">🥇</div>
        <img src="{get_image_url(top_3_produtos.iloc[0])}" width="150"/>
        <div><strong>{top_3_produtos.iloc[0]['name']}</strong></div>
        <div>Score: {top_3_produtos.iloc[0]['score']}</div>
        <div>Reviews: {top_3_produtos.iloc[0]['reviews']}</div>
    </div>
''', unsafe_allow_html=True)

# Segundo lugar
st.markdown(f'''
    <div class="podium-item">
        <div class="medal">🥈</div>
        <img src="{get_image_url(top_3_produtos.iloc[1])}" width="120"/>
        <div><strong>{top_3_produtos.iloc[1]['name']}</strong></div>
        <div>Score: {top_3_produtos.iloc[1]['score']}</div>
        <div>Reviews: {top_3_produtos.iloc[1]['reviews']}</div>
    </div>
''', unsafe_allow_html=True)

# Terceiro lugar
st.markdown(f'''
    <div class="podium-item">
        <div class="medal">🥉</div>
        <img src="{get_image_url(top_3_produtos.iloc[2])}" width="100"/>
        <div><strong>{top_3_produtos.iloc[2]['name']}</strong></div>
        <div>Score: {top_3_produtos.iloc[2]['score']}</div>
        <div>Reviews: {top_3_produtos.iloc[2]['reviews']}</div>
    </div>
''', unsafe_allow_html=True)

# Fechar o container da tabela de pódio
st.markdown('</div>', unsafe_allow_html=True)

# Exibir tabela com os produtos mais bem ranqueados no score combinado
st.subheader("Top Produtos pelo Score Combinado")
top_produtos_score_combinado = df_filtered.nlargest(10, 'score_combinado')
st.dataframe(top_produtos_score_combinado[['name', 'category', 'value', 'reviews', 'score', 'score_combinado']])
