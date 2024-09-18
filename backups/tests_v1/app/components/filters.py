# filters.py
import pandas as pd

def apply_filters(df, date_range, min_value, max_value, selected_category, keyword, min_score, max_score):
    """
    Aplica filtros ao DataFrame com base nos parâmetros selecionados pelo usuário.
    """
    if selected_category == 'Todas as Categorias':
        df_filtered = df[
            (df['value'] >= min_value) &
            (df['value'] <= max_value) &
            (df['score'] >= min_score) &
            (df['score'] <= max_score) &
            (df['date'] >= pd.to_datetime(date_range[0])) &
            (df['date'] <= pd.to_datetime(date_range[1]))
        ]
    else:
        df_filtered = df[
            (df['value'] >= min_value) &
            (df['value'] <= max_value) &
            (df['category'] == selected_category) &
            (df['score'] >= min_score) &
            (df['score'] <= max_score) &
            (df['date'] >= pd.to_datetime(date_range[0])) &
            (df['date'] <= pd.to_datetime(date_range[1]))
        ]

    if keyword:
        df_filtered = df_filtered[df_filtered['name'].str.contains(keyword, case=False, na=False)]

    return df_filtered
