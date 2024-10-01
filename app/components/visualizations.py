# visualizations.py
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

def render_pareto_chart(df_filtered):
    if df_filtered.empty:
        st.warning("Nenhum dado disponível para o gráfico de Pareto.")
        return

    # Agrupamento e cálculo da média de score por categoria
    pareto_chart = df_filtered.groupby('category')['score'].quantile(0.75).reset_index()
    pareto_chart = pareto_chart.sort_values(by='score', ascending=False)

    if pareto_chart.empty:
        st.warning("Dados insuficientes para renderizar o gráfico de Pareto.")
        return

    # Calcular o acumulado percentual
    pareto_chart['acumulado'] = pareto_chart['score'].cumsum() / pareto_chart['score'].sum() * 100

    # Criar gráfico de Pareto
    fig_pareto = go.Figure()

    # Adicionar gráfico de barras para a média de score por categoria
    fig_pareto.add_trace(go.Bar(
        x=pareto_chart['category'], y=pareto_chart['score'], name='3° quartil Score',
        marker_color='rgb(55, 83, 109)', text=pareto_chart['score'].round(2),
        hovertemplate="Categoria: %{x}<br>Média de Score: %{y}"
    ))

    # Adicionar a linha de 80% acumulado
    fig_pareto.add_trace(go.Scatter(
        x=pareto_chart['category'], y=pareto_chart['acumulado'], name='Acumulado %',
        yaxis='y2', marker_color='rgb(26, 118, 255)', mode='lines+markers',
        hovertemplate="Categoria: %{x}<br>Acumulado: %{y:.2f}%"
    ))

    # Definir o layout do gráfico de Pareto
    fig_pareto.update_layout(
        yaxis=dict(title='3° quartil Score'),
        yaxis2=dict(title='Acumulado %', overlaying='y', side='right', range=[0, 100]),
        template='plotly_dark',
        showlegend=True
    )

    st.plotly_chart(fig_pareto, use_container_width=True)

def exibir_analise_preco(df):
    """
    Função para exibir a análise de preço por produto em uma página do Streamlit.
    
    Parâmetros:
    df: DataFrame com os dados de preços e datas para cada produto.
    """
    
    # Título estilizado
    #st.markdown("<div class='section-title'>ANÁLISE DE PREÇO POR PRODUTO</div>", unsafe_allow_html=True)

    # Adicionar a opção de "Todos os produtos"
    produtos_disponiveis = ['Todos'] + df['name'].unique().tolist()

    # Selecionar o produto
    produto_selecionado = st.selectbox('Selecione o produto para visualizar a variação do preço:', produtos_disponiveis)

    # Filtrar os dados
    if produto_selecionado == 'Todos':
        df_filtrado = df  # Seleciona todos os produtos
    else:
        df_filtrado = df[df['name'] == produto_selecionado]  # Filtra pelo produto selecionado

    # Calculando o valor atual (preço na data máxima)
    data_maxima = df_filtrado['date'].max()  # Encontrar a data máxima
    valor_atual = df_filtrado[df_filtrado['date'] == data_maxima]['value'].values[0]  # Valor do produto na data máxima
    min_value = df_filtrado['value'].min()  # Valor mínimo
    max_value = df_filtrado['value'].max()  # Valor máximo

    # Calcular o valor médio por dia
    df_media_diaria = df_filtrado.groupby('date').agg(media_diaria=('value', 'mean')).reset_index()

    # Calcular as estatísticas
    df_stats = df_filtrado.groupby('name').agg(
        media_value=('value', 'mean'),
        mediana_value=('value', 'median'),
        desvio_padrao=('value', 'std'),
        valor_min=('value', 'min'),
        valor_max=('value', 'max'),
        #primeiro_quartil=('value', lambda x: x.quantile(0.25)),
        #terceiro_quartil=('value', lambda x: x.quantile(0.75)),
        amplitude=('value', lambda x: x.max() - x.min())  # Cálculo da amplitude
    ).reset_index()

    # Exibir a tabela de estatísticas no Streamlit
    st.dataframe(df_stats[['name', 'media_value', 'mediana_value', 'desvio_padrao', 'valor_min', 'valor_max', 'amplitude']].sort_values(by='media_value', ascending=False))

    # Exibir o gráfico de linha se um produto específico for selecionado
    if produto_selecionado != 'Todos':
        # Gerar o gráfico de linha para o produto selecionado, com média diária
        fig = px.line(df_media_diaria, x='date', y='media_diaria', title=f'Variação de Preço (Média Diária) para {produto_selecionado}', labels={'media_diaria': 'Preço Médio', 'date': 'Data'})
        
        # Calcular a mediana do valor diário
        mediana_valor = df_filtrado['value'].median()

        # Adicionar uma linha da mediana ao gráfico
        fig.add_trace(
            go.Scatter(
                x=df_media_diaria['date'], 
                y=[mediana_valor] * len(df_media_diaria),  # Repete a mediana para cada data
                mode='lines',
                name='Mediana',
                line=dict(color='red', dash='dash')  # Linha tracejada em vermelho
            )
        )

        # Exibir o gráfico abaixo da tabela
        st.plotly_chart(fig)