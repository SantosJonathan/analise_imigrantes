import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(layout='wide')

st.title('DASHBOARD DE IMIGRAÇÃO DO BRASIL PARA O CANADA')


# LEITURA DOS DADOS VIA PANDAS 
dados = pd.read_csv(r'C:\Users\Jonathan\OneDrive\Área de Trabalho\analise_imigrantes\dados\imigrantes_canada.csv')

# DEFININDO A COLUNA PAÍS COMO INDEX DO MEU DF
dados.set_index('País', inplace=True)

# CRIAR UMA VARIAVEL PARA ARMANEZAR O INTERVALO DE TEMPO "ANOS" (COLUNAS) ISSO VAI FACILITAR NA HORA DE VISUALIZAR OS DADOS
anos = list(map(str, range(1980, 2014)))

# FAZENDO UM FILTRO NO DF PARA PEGAR SOMENTE OS DADOS DO BRASIL - USANDO A FUNÇÃO LOC DO PANDAS
brasil = dados.loc['Brasil', anos]

# CRIAR UM DICIONÁRIO PARA ARMAZENAR AS SERIES QUE FORAM CRIADAS NA VÁRIAVEL ANTERIOR
brasil_dict = {'ano': brasil.index.tolist(), 'imigrantes': brasil.values.tolist()}
df_brasil = pd.DataFrame(brasil_dict)


# GRÁFICOS 

fig_linha = px.line(df_brasil,
                    x='ano',
                    y='imigrantes',
                    markers=True,
                    range_y=(0, df_brasil.max()),
                    range_x=(1980, df_brasil.max()),
                    title='Imigração do Brasil para o Canadá no período de 1980 a 2013')

fig_linha.update_traces(line_color='red', line_width=2)

fig_linha.update_layout(width=800, height=400,
                        yaxis_title='Número de Imigrantes',
                        xaxis_title='Ano',
                        font_family='Arial',
                        font_size=14,
                        font_color='grey',
                        title_font_color='black',
                        title_font_size=22
                        )


# Visualização no streamlit
st.plotly_chart(fig_linha)



#st.dataframe(df_brasil)