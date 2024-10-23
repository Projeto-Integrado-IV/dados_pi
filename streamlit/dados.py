import pandas as pd

# Definir a URL do arquivo CSV
url_saneamento = 'https://github.com/Projeto-Integrado-IV/dados_pi/raw/refs/heads/main/raw/base_saneamento_tratada.csv'

# Ler o arquivo CSV
df_saneamento = pd.read_csv(url_saneamento, delimiter=';', encoding='latin1')

# Selecionar as colunas necessárias e renomear a coluna 'Código IBGE'
df_saneamento = df_saneamento[['Cidade', 'População em 2021', 'Código IBGE', 'Área Territorial - km2']].rename(columns={'Código IBGE': 'cod_ibge', 'População em 2021': 'populacao', 'Área Territorial - km2': 'area_territorial'})

# Definir a URL do arquivo CSV
url_mortalidade = 'https://github.com/Projeto-Integrado-IV/dados_pi/raw/refs/heads/main/raw/obitosinfantis_periodo_tratada.csv'

# Ler o arquivo CSV
df_mortalidade = pd.read_csv(url_mortalidade, delimiter=';', encoding='latin1')

# Remover a linha onde 'cod_ibge' é igual a 3500000
df_mortalidade = df_mortalidade[df_mortalidade['cod_ibge'] != 3500000]

# Realizar o join usando a chave 'cod_ibge' de cada DataFrame
df = pd.merge(df_mortalidade, df_saneamento, on='cod_ibge', how='left')

# Ordernação do DataFrame
df = df[['Cidade', 'cod_ibge', 'populacao', 'area_territorial', 'ano', 'nascidos vivos (por local de residência)', 'obitos menores de 1 Ano', 'obitos menores de 7 dias', 'obitos de 28 dias a 364 dias', 'obitos de 7 a 27 dias']]