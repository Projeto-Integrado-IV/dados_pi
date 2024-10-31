import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
import numpy as np

from dados import df

st.set_page_config(
    page_title="Projeto Integrado - Análise de Mortalidade Infantil", 
    page_icon="📊"
)

# Título da aplicação
st.title("Dados de Mortalidade Infantil")

# Seleção de cidades no menu lateral
cidades = df['Cidade'].unique()
cidades_selecionadas = st.multiselect("Selecione um ou mais Municípios:", cidades)

# Sidebar para seleção de cidade e parâmetros de ML
st.sidebar.title("Configurações de Aprendizagem de Maquina")

# Parâmetros do modelo na barra lateral
# Explicação sobre o tamanho do teste
st.sidebar.write("O tamanho do teste é a fração dos dados que será utilizada para avaliar o modelo de aprendizado de máquina. Ajuste o controle deslizante abaixo para definir a proporção dos dados a serem reservados para teste (por exemplo, 20% dos dados).")

# Parâmetros do modelo na barra lateral
test_size = st.sidebar.slider("Tamanho do teste (fração)", min_value=0.1, max_value=0.5, value=0.2, step=0.1)
# Parâmetros do modelo na barra lateral
kernel = st.sidebar.selectbox("Kernel do SVR", options=["linear", "poly", "rbf", "sigmoid"], index=2)

# Explicação do kernel selecionado
if kernel == "linear":
    st.sidebar.write("O kernel linear é uma função que calcula a previsão como uma combinação linear das variáveis de entrada. É ideal para dados que têm uma relação linear clara.")
elif kernel == "poly":
    st.sidebar.write("O kernel polinomial é uma função que calcula a previsão como um polinômio das variáveis de entrada. Ele pode capturar relações não lineares entre as variáveis.")
elif kernel == "rbf":
    st.sidebar.write("O kernel RBF (Radial Basis Function) é uma função que calcula a previsão com base na distância das variáveis de entrada a um ponto central. É útil para capturar complexidades e não linearidades nos dados.")
elif kernel == "sigmoid":
    st.sidebar.write("O kernel sigmoid é uma função que imita a função de ativação sigmoide. É menos comum em SVR, mas pode ser usado para capturar certas relações não lineares.")

# Filtrando o DataFrame com base nas cidades selecionadas
df_filtrado = df[df['Cidade'].isin(cidades_selecionadas)]

# Exibindo informações dos municípios selecionados na barra lateral
with st.expander("Informações sobre os municípios", expanded=True):
    for cidade in cidades_selecionadas:
        df_cidade = df_filtrado[df_filtrado['Cidade'] == cidade]
        area = df_cidade['area_territorial'].values[0] if not df_cidade.empty else 'N/A'
        populacao = df_cidade['populacao'].values[0] if not df_cidade.empty else 'N/A'
        
        # Formatação compacta e visualmente agradável
        st.markdown(f"### {cidade}")
        st.markdown(f"**Área Territorial:** {area} km² | **População Urbana:** {populacao}")
        st.write("---")



if not df_filtrado.empty:
    st.subheader("Gráfico de Mortalidade Infantil com Previsões")

    # Gráfico inicial
    fig3 = px.line(title='Taxa de Mortalidade Infantil por Município com Previsões',
                   labels={'ano': 'Ano', 'taxa_mortalidade_infantil': 'Taxa de Mortalidade Infantil (por 1000 nascidos vivos)'})

    for cidade in cidades_selecionadas:
        # Filtrar os dados por cidade
        df_cidade = df_filtrado[df_filtrado['Cidade'] == cidade]

        # Calcular a taxa de mortalidade infantil
        if 'obitos menores de 1 Ano' in df_cidade.columns and 'nascidos vivos (por local de residência)' in df_cidade.columns:
            df_cidade['taxa_mortalidade_infantil'] = (df_cidade['obitos menores de 1 Ano'] / df_cidade['nascidos vivos (por local de residência)']) * 1000
        else:
            st.warning(f"Dados insuficientes para calcular a taxa de mortalidade infantil para {cidade}.")
            continue  # Pula para a próxima cidade

        # Remover linhas com valores NaN em 'ano' ou 'taxa_mortalidade_infantil'
        df_cidade = df_cidade.dropna(subset=['ano', 'taxa_mortalidade_infantil'])

        # Verifica se ainda existem dados após a remoção
        if df_cidade.empty:
            st.warning(f"Sem dados disponíveis para {cidade} após filtragem.")
            continue  # Pula para a próxima cidade

        # Preparar dados para o modelo de aprendizado de máquina
        X = df_cidade[['ano']].values  # Variável independente (ano)
        y = df_cidade['taxa_mortalidade_infantil'].values  # Variável dependente

        # Dividir dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

        # Treinar o modelo SVR
        model_svr = SVR(kernel=kernel)
        model_svr.fit(X_train, y_train)

        # Prever valores para os anos futuros (2022 a 2030)
        anos_futuros = np.array([[ano] for ano in range(2022, 2031)])
        previsoes_futuras = model_svr.predict(anos_futuros)

        # Adicionar dados históricos e previsões ao gráfico
        fig3.add_scatter(x=df_cidade['ano'], y=df_cidade['taxa_mortalidade_infantil'], mode='lines+markers', name=f'{cidade} - Dados Reais')
        fig3.add_scatter(x=anos_futuros.flatten(), y=previsoes_futuras, mode='lines+markers', name=f'{cidade} - Previsão', line=dict(dash='dash'))

        # Gráfico de óbitos menores de 1 ano
    fig1 = px.line(df_filtrado, x='ano', y='obitos menores de 1 Ano', color='Cidade', title='Óbitos Menores de 1 Ano', labels={'ano': 'Ano', 'obitos menores de 1 Ano': 'Óbitos Menores de 1 Ano'}, line_shape='linear')


    # Gráfico de nascimentos
    fig2 = px.line(df_filtrado, x='ano', y='nascidos vivos (por local de residência)', color='Cidade', title='Nascidos Vivos', labels={'ano': 'Ano', 'nascidos vivos (por local de residência)': 'Nascidos Vivos'}, line_shape='linear')


    # Adicionar zonas de classificação
    fig3.add_shape(type="rect", x0=df_filtrado['ano'].min(), y0=50, x1=2030, y1=215, fillcolor="red", opacity=0.2, layer="below", line_width=0, name="Alta (50 ou mais)")
    fig3.add_shape(type="rect", x0=df_filtrado['ano'].min(), y0=20, x1=2030, y1=50, fillcolor="Orange", opacity=0.2, layer="below", line_width=0, name="Média (20-49)")
    fig3.add_shape(type="rect", x0=df_filtrado['ano'].min(), y0=0, x1=2030, y1=20, fillcolor="Green", opacity=0.2, layer="below", line_width=0, name="Baixa (menos de 20)")

    # Legenda das zonas de classificação
    fig3.update_layout(
        annotations=[
            dict(x=2030, y=75, xref="x", yref="y", text="Alta (50 ou mais)", showarrow=False, font=dict(color="Red")),
            dict(x=2030, y=35, xref="x", yref="y", text="Média (20-49)", showarrow=False, font=dict(color="Orange")),
            dict(x=2030, y=10, xref="x", yref="y", text="Baixa (menos de 20)", showarrow=False, font=dict(color="Green"))
        ]
    )

    # Exibir o gráfico com dados reais e previsões
    st.plotly_chart(fig3)
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

    # Exibição da tabela de dados filtrados
    st.subheader("Tabela de Dados de Mortalidade Infantil")
    st.dataframe(df_filtrado.style.set_caption("Dados Filtrados de Mortalidade Infantil").set_table_styles(
        [{'selector': 'th', 'props': [('max-width', '200px')]}]))



st.markdown(
    "Fonte dos dados: [Mortalidade Infantil - SEADE](https://repositorio.seade.gov.br/dataset/mortalidade-infantil)"
)
