# visualizations.py
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def render_pareto_chart(df_filtered):
    """
    Renderiza o gráfico de Pareto baseado na média de score por categoria.
    """
    pareto_chart = df_filtered.groupby('category')['score'].mean().reset_index()
    pareto_chart = pareto_chart.sort_values(by='score', ascending=False)

    # Calcular o acumulado percentual
    pareto_chart['acumulado'] = pareto_chart['score'].cumsum() / pareto_chart['score'].sum() * 100

    # Criar gráfico de Pareto
    fig_pareto = go.Figure()

    # Adicionar gráfico de barras para a média de score por categoria
    fig_pareto.add_trace(go.Bar(
        x=pareto_chart['category'], y=pareto_chart['score'], name='Média de Score',
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
        title="Pareto da Média de Score por Categoria",
        yaxis=dict(title='Média de Score'),
        yaxis2=dict(title='Acumulado %', overlaying='y', side='right', range=[0, 100]),
        template='plotly_dark',
        showlegend=True
    )

    st.plotly_chart(fig_pareto, use_container_width=True)
