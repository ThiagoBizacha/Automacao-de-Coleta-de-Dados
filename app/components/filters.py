import streamlit as st
import pandas as pd

def apply_filters(df, date_range=None, min_value=None, max_value=None, selected_categories=None, keyword=None, min_score=None, max_score=None):
    # Filtrar pelo intervalo de datas
    df = df[
        (df['date'] >= pd.to_datetime(date_range[0])) &
        (df['date'] <= pd.to_datetime(date_range[1]))
    ]

    # Filtrar pelo intervalo de valor (value)
    if min_value is not None and max_value is not None:
        df = df[(df['value'] >= min_value) & (df['value'] <= max_value)]

    # Filtrar pelas categorias selecionadas
    if selected_categories and 'Todas as Categorias' not in selected_categories:
        df = df[df['category'].isin(selected_categories)]  # Alterado para verificar se a categoria está na lista selecionada

    # Filtrar pela palavra-chave no nome do produto
    if keyword:
        df = df[df['name'].str.contains(keyword, case=False, na=False)]

    # Filtrar pelo intervalo de score (se aplicável)
    if min_score is not None and max_score is not None:
        df = df[(df['score'] >= min_score) & (df['score'] <= max_score)]

    return df

