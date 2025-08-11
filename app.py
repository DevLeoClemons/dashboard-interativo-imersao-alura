import streamlit as st
import pandas as pd 
import plotly.express as px

# 1️⃣ Primeiro comando Streamlit tem que ser set_page_config
st.set_page_config(
    page_title='Dashboard de Salários na Área de dados',
    page_icon='📊',
    layout='wide'
)
st.markdown("""
    <style>
    /* Tags selecionadas do multiselect na sidebar */
    section[data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: #2c7be5 !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        padding: 0.12rem 0.5rem !important;
        display: inline-flex !important;
        align-items: center !important;
        margin: 0 4px 4px 0 !important;
    }

    /* Texto interno das tags */
    section[data-testid="stSidebar"] [data-baseweb="tag"] span {
        color: #ffffff !important;
    }

    /* Botão 'x' dentro da tag */
    section[data-testid="stSidebar"] [data-baseweb="tag"] button {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    /* Caixa do multiselect no sidebar (fundo e borda) */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div:first-child {
        background-color: var(--sidebar-background-color) !important;
        border-radius: 6px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    /* Borda ao focar no multiselect (usar azul, não vermelho) */
    section[data-testid="stSidebar"] div[data-baseweb="select"]:focus-within > div:first-child {
        border: 1px solid #2c7be5 !important;
        box-shadow: 0 0 0 1px #2c7be5 !important;
    }

    /* Itens dropdown hover/selecionados */
    section[data-testid="stSidebar"] div[data-baseweb="select"] ul li:hover,
    section[data-testid="stSidebar"] div[data-baseweb="select"] ul li[aria-selected="true"],
    section[data-testid="stSidebar"] div[data-baseweb="select"] ul li[data-highlighted="true"] {
        background-color: #2c7be5 !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)






# ... resto do seu código

df = pd.read_csv('dados-imersao-final.csv')

st.sidebar.header('🔍 Filtros')

# Filtro de Ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect('Ano', anos_disponiveis, default=anos_disponiveis)

# Filtro de Senioridade
Senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect('Senioridade', Senioridades_disponiveis, default=Senioridades_disponiveis)

# Filtro de Contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect('Tipo de Contrato', contratos_disponiveis, default=contratos_disponiveis)

# Filtro por tamanho da empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect('Porte da Empresa', tamanhos_disponiveis, default=tamanhos_disponiveis)

# Filtragem do DataFrame
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

# Conteúdo principal
st.title('🎲 Análise de Salários na Área de Dados - By Leo Clemons')
st.markdown('Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros da barra lateral à esquerda para refinar sua análise.')

st.subheader('Métricas gerais (Salário anual em USD)')

if not df_filtrado.empty:
    salario_medio = df_filtrado['salario_anual_conv_usd'].mean()
    salario_maximo = df_filtrado['salario_anual_conv_usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
    salario_medio, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, ''

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,.0f}".replace(',', '.'))
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown('---')

st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['salario_anual_conv_usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='salario_anual_conv_usd',
            y='cargo',
            orientation='h',
            title='Top 10 cargos por salário médio',
            labels={'salario_anual_conv_usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir no gráfico de cargos.')

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='salario_anual_conv_usd',
            nbins=30,
            title='Distribuição de salários anuais',
            labels={'salario_anual_conv_usd': 'Faixa salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir no gráfico de distribuição.')

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1, legend={'x':0})
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir no gráfico dos tipos de trabalho.')

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['salario_anual_conv_usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
                    locations='residencia_iso3',
                    color='salario_anual_conv_usd',
                    color_continuous_scale='Blues',
                    title='Salário médio de Cientista de Dados por país',
                    labels={'salario_anual_conv_usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', geo=dict(bgcolor='rgba(0,0,0,0)'))
            # paper_bgcolor → tudo (inclusive margens).
            # plot_bgcolor → área dos dados.
            # geo.bgcolor → fundo da parte geográfica do mapa.
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países")
        
st.subheader('Dados Detalhados')
st.dataframe(df_filtrado)