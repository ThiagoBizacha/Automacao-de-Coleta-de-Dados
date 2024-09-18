# TESTE

PROJETO_AUTOMACAO_COLETA_DADOS/
├── etl/
│   ├── extract/
│   │   └── extract_data_amazon.py          # Scripts de extração de dados (Amazon, APIs, etc.)
│   ├── transform/
│   │   └── transform_data_amazon.py        # Scripts de transformação de dados
│   ├── load/
│   │   ├── load_data_amazon.py             # Scripts de carregamento (ex.: arquivos)
│   │   └── load_postgresql.py              # Scripts para carregar dados no PostgreSQL
│   ├── pipeline/
│   │   └── pipeline_data_amazon.py         # Pipeline completo de execução (Extract -> Transform -> Load)
│   └── tests/
│       └── test_etl_pipeline.py            # Testes relacionados ao ETL
│
├── app/                                    # Diretório do aplicativo Streamlit
│   ├── pages/
│   │   ├── best_sellers.py                 # Página de análise para Best Sellers
│   │   ├── new_releases.py                 # Página de análise para New Releases
│   │   └── movers_and_shakers.py           # Página de análise para Movers and Shakers
│   ├── components/
│   │   ├── filters.py                      # Módulo para aplicar filtros comuns
│   │   ├── kpi_calculator.py               # Módulo para calcular os KPIs
│   │   └── visualizations.py               # Funções de visualização (gráficos, nuvens de palavras, etc.)
│   ├── static/
│   │   ├── styles.css                      # Estilos CSS para o app Streamlit
│   ├── templates/                          # Modelos HTML para relatórios ou visualizações
│   │   ├── index.html
│   │   └── result.html
│   └── app.py                              # Arquivo principal para carregar as páginas do Streamlit
│
├── data/
│   ├── input/                              # Dados de entrada (se houver)
│   ├── output/                             # Dados processados (se houver)
│   └── logs/                               # Logs do sistema
│       └── etl_logs.log                    # Logs do pipeline de ETL
│
├── config/                                 # Arquivos de configuração
│   ├── settings.yaml                       # Configurações gerais (ex.: banco de dados, API keys)
│   └── .env                                # Arquivos de variáveis de ambiente (senhas, tokens, etc.)
│
├── tests/
│   ├── test_app.py                         # Testes para o app Streamlit
│   └── test_visualizations.py              # Testes para visualizações e componentes do app
│
├── venv/                                   # Ambiente virtual para dependências do projeto
├── README.md                               # Documentação do projeto
└── requirements.txt                        # Arquivo de dependências para instalação via pip
