import streamlit as st
import pandas as pd

# Carregando os dados
url = 'https://github.com/Projeto-Integrado-IV/dados_pi/raw/refs/heads/main/raw/base_saneamento_tratada.csv'
df = pd.read_csv(url, delimiter=';', encoding='latin1')

# Título da aplicação
st.title("Dados de Saneamento")

# Sidebar para seleção de método de envio (pode ser ajustado conforme necessidade)
with st.sidebar:
    st.header("Método de Envio")
    add_radio = st.radio(
        "Escolha um método:",
        ("Padrão (5-15 dias)", "Expresso (2-5 dias)")
    )

# Filtrando a coluna 'Cidade'
cidades = df['Cidade'].unique()  # Obtendo as cidades únicas
cidade_selecionada = st.selectbox("Selecione um Município:", cidades)

# Filtrando o DataFrame com base na cidade selecionada
df_filtrado = df[df['Cidade'] == cidade_selecionada]

# Exibindo o DataFrame filtrado
st.subheader(f"Dados para: {cidade_selecionada}")
st.dataframe(df_filtrado)

# Expander para informações sobre o município
with st.expander("Informações sobre o município"):
    area = df_filtrado['Área Territorial - km2'].values[0] if not df_filtrado.empty else 'N/A'
    populacao = df_filtrado['População Urbana - Habitantes'].values[0] if not df_filtrado.empty else 'N/A'
    
    st.write(f"**Área Territorial (km²):** {area}")
    st.write(f"**População Urbana:** {populacao}")

# Adicionando uma visualização adicional, como gráficos (opcional)
if st.checkbox("Mostrar gráfico de população"):
    st.bar_chart(df_filtrado['População Urbana - Habitantes'])  # Exemplo de gráfico