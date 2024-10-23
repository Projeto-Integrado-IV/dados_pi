from dados import df
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Título da aplicação
st.title("Dados de Mortalidade Infantil")

# Filtrando a coluna 'Cidade'
cidades = df['Cidade'].unique()
cidades_selecionadas = st.multiselect("Selecione um ou mais Municípios:", cidades)

# Filtrando o DataFrame com base nas cidades selecionadas
df_filtrado = df[df['Cidade'].isin(cidades_selecionadas)]

# Expander para informações sobre os municípios
with st.expander("Informações sobre os municípios", expanded=True):
    for cidade in cidades_selecionadas:
        df_cidade = df_filtrado[df_filtrado['Cidade'] == cidade]
        area = df_cidade['area_territorial'].values[0] if not df_cidade.empty else 'N/A'
        populacao = df_cidade['populacao'].values[0] if not df_cidade.empty else 'N/A'
        
        st.write(f"### {cidade}")
        st.write(f"**Área Territorial (km²):** {area}")
        st.write(f"**População Urbana:** {populacao}")
        st.write("---")



# Tabela de dados
st.subheader("Tabela de Dados de Mortalidade Infantil")
st.dataframe(df_filtrado.style.set_caption("Dados Filtrados de Mortalidade Infantil").set_table_styles(
    [{'selector': 'th', 'props': [('max-width', '200px')]}]))


# Verificar se o DataFrame não está vazio
if not df_filtrado.empty:
    st.subheader("Gráficos de Mortalidade Infantil")

    # Calcular a taxa de mortalidade infantil
    df_filtrado['taxa_mortalidade_infantil'] = (df_filtrado['obitos menores de 1 Ano'] / df_filtrado['nascidos vivos (por local de residência)']) * 1000

    # Gráfico de óbitos menores de 1 ano
    fig1 = px.line(df_filtrado, x='ano', y='obitos menores de 1 Ano', color='Cidade', title='Óbitos Menores de 1 Ano', labels={'ano': 'Ano', 'obitos menores de 1 Ano': 'Óbitos Menores de 1 Ano'}, line_shape='linear')
    st.plotly_chart(fig1)

    # Gráfico de nascimentos
    fig2 = px.line(df_filtrado, x='ano', y='nascidos vivos (por local de residência)', color='Cidade', title='Nascidos Vivos', labels={'ano': 'Ano', 'nascidos vivos (por local de residência)': 'Nascidos Vivos'}, line_shape='linear')
    st.plotly_chart(fig2)

    # Gráfico de taxa de mortalidade infantil com linhas fixas
    fig3 = px.line(df_filtrado, x='ano', y='taxa_mortalidade_infantil', color='Cidade', title='Taxa de Mortalidade Infantil', labels={'ano': 'Ano', 'taxa_mortalidade_infantil': 'Taxa de Mortalidade Infantil (por 1000 nascidos vivos)'}, line_shape='linear')

    # Adicionar linhas fixas para as classificações
    fig3.add_shape(type="line", x0=df_filtrado['ano'].min(), y0=50, x1=df_filtrado['ano'].max(), y1=50, line=dict(color="Red", width=2, dash="dash"), name="Alta (50 ou mais)")
    fig3.add_shape(type="line", x0=df_filtrado['ano'].min(), y0=20, x1=df_filtrado['ano'].max(), y1=20, line=dict(color="Orange", width=2, dash="dash"), name="Média (20-49)")
    fig3.add_shape(type="line", x0=df_filtrado['ano'].min(), y0=0, x1=df_filtrado['ano'].max(), y1=0, line=dict(color="Green", width=2, dash="dash"), name="Baixa (menos de 20)")

    # Atualizar layout para incluir legenda das linhas fixas
    fig3.update_layout(
        shapes=[
            dict(type="line", x0=df_filtrado['ano'].min(), y0=50, x1=df_filtrado['ano'].max(), y1=50, line=dict(color="Red", width=2, dash="dash")),
            dict(type="line", x0=df_filtrado['ano'].min(), y0=20, x1=df_filtrado['ano'].max(), y1=20, line=dict(color="Orange", width=2, dash="dash")),
            dict(type="line", x0=df_filtrado['ano'].min(), y0=0, x1=df_filtrado['ano'].max(), y1=0, line=dict(color="Green", width=2, dash="dash"))
        ],
        annotations=[
            dict(x=df_filtrado['ano'].max(), y=50, xref="x", yref="y", text="Alta (50 ou mais)", showarrow=True, arrowhead=7, ax=0, ay=-40),
            dict(x=df_filtrado['ano'].max(), y=20, xref="x", yref="y", text="Média (20-49)", showarrow=True, arrowhead=7, ax=0, ay=-40),
            dict(x=df_filtrado['ano'].max(), y=0, xref="x", yref="y", text="Baixa (menos de 20)", showarrow=True, arrowhead=7, ax=0, ay=-40)
        ]
    )

    st.plotly_chart(fig3)