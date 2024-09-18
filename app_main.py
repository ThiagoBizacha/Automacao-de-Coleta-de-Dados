import streamlit as st
from streamlit_option_menu import option_menu

# Configuração de layout
st.set_page_config(page_title="Análise Estratégica de Dados Amazon", layout="wide", page_icon="📊")

# Melhorar a aparência do menu
with st.sidebar:
    menu = option_menu(
        "Navegação", 
        ['Best Sellers', 'New Releases', 'Movers and Shakers'],  # Páginas
        icons=['star', 'gift', 'bar-chart-line'],  # Ícones melhorados, troquei 'trending-up' por 'bar-chart-line'
        menu_icon="cast",  # Ícone do menu principal
        default_index=0,  # Página inicial
    )

# Importar as páginas correspondentes com base na seleção do usuário
if menu == 'Best Sellers':
    import app.pages.best_sellers as best_sellers
    best_sellers.show_page()

elif menu == 'New Releases':
    import app.pages.new_releases as new_releases
    new_releases.show_page()

elif menu == 'Movers and Shakers':
    import app.pages.movers_and_shakers as movers_and_shakers
    movers_and_shakers.show_page()
