import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

st.set_page_config(layout='wide')

anos_selecionados = ['2019','2020','2021','2022','2023']

# Definir um dicionário de mapeamento
meses = {
    '01': 'janeiro',
    '02': 'fevereiro',
    '03': 'março',
    '04': 'abril',
    '05': 'maio',
    '06': 'junho',
    '07': 'julho',
    '08': 'agosto',
    '09': 'setembro',
    '10': 'outubro',
    '11': 'novembro',
    '12': 'dezembro'
}

# Cria a nova coluna usando a função map e o dicionário de mapeamento
#df['mes_extenso'] = df['mes'].map(meses)




st.title('Evolução do Índice de Inflação no Brasil (IPCA)')
st.caption('Índice de Preços ao Consumidor Amplo')




dados = pd.read_csv(r'C:\Users\Jonathan\OneDrive\Área de Trabalho\analise_imigrantes\dados\inflacao.csv')

dados = pd.DataFrame(dados)

# Criando um DF somente com os dados do IPCA / TX SELIC / JUROS E SM
df_ipca = dados[['ipca_variacao','ipca_acumulado_ano','ipca_acumulado_doze_meses','selic_meta','selic_ano','juros_reais','salario_minimo']]

# CRIANDO A COLUNA MêS E ANO A PARTIR DA COLUNA REFERENCIA
df_ipca['ano'] = dados['referencia'].apply(lambda x: x[:4])

df_ipca['mes'] = dados['referencia'].apply(lambda x: x[-2:]).map(meses)

# FILTRO DOS ÚLTIMOS 10 ANOS
df_ipca = df_ipca.loc[df_ipca['ano'].isin(anos_selecionados)]


df_ipca['Ano'] = pd.to_datetime(df_ipca['ano'])
df_ipca['Ano'] = df_ipca['Ano'].dt.year
df_ipca['Ano'] = np.floor(df_ipca['Ano'])


# Criar tabelas

# _IPCA TOTAL ANO

ipca_variacao_ano = df_ipca.groupby('Ano')[['ipca_variacao']].sum().reset_index()


# Criar Gráficos 
fig_ipca_ano = px.line(ipca_variacao_ano,
                        x='Ano',
                        y='ipca_variacao',
                        markers=True,
                        range_y=(0, ipca_variacao_ano.max()),
                       
                       title='IPCA - Acumulado nos últimos 5 ano')

fig_ipca_ano.update_traces(line_color='grey', line_width=3)

fig_ipca_ano.update_layout(width=500, height=300,
                        yaxis_title='',
                        xaxis_title='Ano',
                        font_family='Arial',
                        font_size=14,
                        font_color='grey',
                        title_font_color='black',
                        title_font_size=22
                        )




# Visualização no streamlit

st.plotly_chart(fig_ipca_ano)




ipca_variacao_ano.info()



#st.dataframe(ipca_variacao_ano)

st.dataframe(df_ipca)