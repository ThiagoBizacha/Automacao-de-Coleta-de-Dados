import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path para encontrar o módulo 'config'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Carregar as configurações do ambiente
from config.environment_setup import get_environment_settings
get_environment_settings()

import streamlit as st
from streamlit_option_menu import option_menu
import base64

# Configuração de layout
st.set_page_config(page_title="Análise Estratégica de Dados Amazon", layout="wide", page_icon="📊")

# Função para carregar o CSS do arquivo externo
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carregar o arquivo styles.css da pasta static
css_file = os.path.join(os.path.dirname(__file__), 'app', 'static', 'styles.css')
load_css(css_file)

#----------------------------------------------------------------------------------------------------------------------------------
# Melhorar a aparência do menu
#----------------------------------------------------------------------------------------------------------------------------------

# Melhorar a aparência do menu com mais estilo e ajustes profissionais
with st.sidebar:
    menu = option_menu(
        "Amazon.nl", 
        ['Principal', 'Benchmark', 'Desenvolvimentos',],  # Páginas principais
        icons=['house', 'tools', 'bar-chart'],  # Ícones representando as páginas
        menu_icon="cast",  # Ícone do menu principal
        default_index=0,  # Página inicial
        styles={
            "container": {
                "padding": "0!important", 
                "background-color": "#262730",  # Cor de fundo mais suave
                "border-radius": "12px",  # Bordas arredondadas para um visual moderno
                "margin": "10px"
            },
            "icon": {
                "color": "#00FFAA", 
                "font-size": "22px"  # Ícones com tamanho ajustado para elegância
            },
            "nav-link": {
                "font-size": "18px",  # Tamanho adequado da fonte para legibilidade
                "color": "#FFFFFF",  # Texto branco em fundo escuro
                "padding": "12px 20px",  # Mais espaçamento entre os itens
                "margin": "5px 0",
                "text-align": "left",
                "border-radius": "8px",  # Borda suave para os links
                "transition": "all 0.3s ease-in-out",  # Suavidade nas transições
                "--hover-color": "#1C1C1C",  # Cor de destaque ao passar o mouse
                "--hover-box-shadow": "0 4px 10px rgba(0, 0, 0, 0.3)",  # Sombra suave ao passar o mouse
            },
            "nav-link-selected": {
                "background-color": "#1C1C1C",  # Cor verde para destacar o item selecionado
                "font-weight": "bold",  # Negrito para ênfase
                #"box-shadow": "0 4px 12px rgba(0, 255, 136, 0.3)",  # Sombra suave para o item selecionado
                #"color": "#FFFFFF"
            },
            "nav-link:hover": {
                #"background-color": "#ff5733",  # Cor de hover para um efeito de destaque
                #"color": "#FFFFFF"
            }
        }
    )

#----------------------------------------------------------------------------------------------------------------------------------
# Página Principal com Subpastas (Best Sellers, New Releases, Movers and Shakers)
#----------------------------------------------------------------------------------------------------------------------------------

if menu == 'Principal':
    # Título da página com data
    st.markdown(f"""
        <div class="title-container">
            <div class="title-left">DADOS AMAZON.NL - BETA</div>
            <div class="separator"></div>
        </div>
    """, unsafe_allow_html=True)

    # Criando Abas/Subpastas para a página Principal
    tab1, tab2, tab3 = st.tabs(["Best Sellers", "New Releases", "Movers and Shakers"])

    with tab1:
        import app.pages.best_sellers as best_sellers
        best_sellers.show_page()

    with tab2:
        import app.pages.new_releases as new_releases
        new_releases.show_page()

    with tab3:
        import app.pages.movers_and_shakers as movers_and_shakers
        movers_and_shakers.show_page()
#------------------------------------------------------------------------------------------------------------------------------------------

# Página Próximos Desenvolvimentos com Subpastas (Integrações, Tendências, Novos KPIs, IA)
if menu == 'Desenvolvimentos':
    st.markdown("<h1 class='title-left'>Próximos Desenvolvimentos</h1>", unsafe_allow_html=True)

    # Criando Abas/Subpastas para Próximos Desenvolvimentos
    tab1, tab2, tab3, tab4 = st.tabs(["Fase 1", "Fase 2", "Fase 3", "Fase 4"])

    # Conteúdo da primeira aba "Fase 1"
    with tab1:
        st.markdown("<h2 class='section-title'>Fase 1 - Entregáveis - OK</h2>", unsafe_allow_html=True)

        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>Total de horas de desenvolvimento: 40h</h3>
         </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>OK - Desenvolvimento de API para Amazon.nl:</h3>
            <p class='highlight-details'>
                Implementação de uma API que realiza a extração dos produtos mais vendidos, novos lançamentos e produtos em alta por categoria.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>OK - Relatórios e Indicadores da Amazon.nl:</h3>
            <p class='highlight-details'>
                Extração de 2.700 produtos da Amazon.nl em agosto de 2024, seguido pelo processamento e organização dos dados para geração de relatórios. 
                Desenvolvemos indicadores-chave como Score (valor percebido), satisfação do cliente, market share e popularidade, para fornecer insights estratégicos.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>OK - Estudo e Análise Estratégica de Mercado:</h3>
            <p class='highlight-details'>
                Condução de uma análise abrangente utilizando artigos, blogs, pesquisas no Shopify e análises no Google Trends, para identificar os principais 
                nichos e produtos no e-commerce, assim como seu histórico de pesquisas na web.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Conteúdo da segunda aba "Fase 2"
    with tab2:
        st.markdown("<h2 class='section-title'>Fase 2 - Back-end e automação</h2>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>Total de horas de desenvolvimento: 60h</h3>
         </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>OK - Automatização da Execução Diária:</h3>
            <p class='highlight-details'>
                Desenvolver um sistema automatizado que realiza a extração diária de dados da Amazon.nl através de um servidor dedicado.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>OK - Tratamento e limpeza dos dados coletados:</h3>
            <p class='highlight-details'>
                Desenvolvimento de um Pipeline para tratar os dados brutos de forma automatizada.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>OK - Criação de Banco de Dados:</h3>
            <p class='highlight-details'>
                Implementar um banco de dados no servidor para armazenar, processar todos os dados coletados.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>OK - Geração Automática de Relatórios e Insights:</h3>
            <p class='highlight-details'>
                Automatizar a criação de relatórios diários baseados nos dados extraídos, com indicadores como popularidade e Score. 
                Esses relatórios auxiliarão na tomada de decisões estratégicas baseadas na análise de Pareto.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Conteúdo da terceira aba "Fase 3"
    with tab3:
        st.markdown("<h2 class='section-title'>Fase 3 - Front-end e Novas Integrações</h2>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>OK - Front-end:</h3>
            <p class='highlight-details'>
                Desenvolver uma aplicação web customizada para analisar e consultar os dados
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>Integração com Bol.com:</h3>
            <p class='highlight-details'>
                Desenvolver uma API que permita a extração de dados e termos de busca do site de e-commerce Bol.com.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>Google Trends:</h3>
            <p class='highlight-details'>
                Implementar uma API para acessar o histórico e as tendências de busca na Holanda (Europa) ou qualquer outro mercado desejado, por meio de palavras-chave.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>Vinculação de Dados:</h3>
            <p class='highlight-details'>
                Conectar dados da Amazon com Google Trends e Bol.com para fornecer insights mais detalhados e integrados.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Conteúdo da quarta aba "Fase 4"
    with tab4:
        st.markdown("<h2 class='section-title'>Fase 4 - Web App/IA</h2>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>Implementação de um Web App:</h3>
            <p class='highlight-details'>
                Alocar o portal em um servidor que permite ao usuário analisar dados de períodos específicos, visualizar indicadores graficamente, buscar por palavras-chave e selecionar plataformas de pesquisa como Amazon, Bol.com e Google Trends para obter insights personalizados.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='highlight-box'>
            <h3 class='highlight-title'>Uso de IA para Análise:</h3>
            <p class='highlight-details'>
                Utilizar inteligência artificial para processar grandes volumes de dados, oferecendo previsões de demanda e recomendações inteligentes baseadas em padrões encontrados.
            </p>
        </div>
        """, unsafe_allow_html=True)

#-------------------------------------------------------------------------------------------------------------------------------------
# Página Benchmark com Subpastas (Shopify, AliExpress)
if menu == 'Benchmark':
    st.markdown("<h1 class='title-left'>Benchmark</h1>", unsafe_allow_html=True)

    # Criando Abas/Subpastas para Benchmark
    tab1, tab2 = st.tabs(["Análise de mercado", "AliExpress"])

    with tab1:
        st.markdown("<h2 class='section-title'>Análise de mercado</h2>", unsafe_allow_html=True)
        st.write("Aqui está uma pesquisa de mercado e análise de Benchmark para Shopify...")

        # Visualização do PDF diretamente na página
        pdf_path = "C:\\Users\\ThiagoBizacha\\Desktop\\Projeto_Automacao_Coleta_Dados\\docs\Apresentações\\Relatorio Identificação de Nichos e Produtos.pdf"
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1650" height="2000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    with tab2:
        st.header("AliExpress")
        st.write("Aqui está a análise de Benchmark para AliExpress...")
