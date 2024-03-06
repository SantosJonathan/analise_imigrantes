import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time
from sklearn.linear_model import LinearRegression



# Interface APP
st.set_page_config(layout='wide',
                   page_title="Estudo de Despesas do Condomínio",
                   initial_sidebar_state="auto",                   
                   )

st.title(':white[Estudo de Despesas do Condomínio - Mauricio Troncho de Melo]')
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

meses = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}

def format_numero(valor, prefixo=''):
    escalas = ['', 'mil', 'milhões', 'bilhões']
    escala_index = 0

    while valor >= 1000 and escala_index < len(escalas):
        valor /= 1000
        escala_index += 1

    return f'{prefixo} {valor:.2f} {escalas[escala_index]}'



# Dados
dados = pd.read_csv(r'C:\Users\Jonathan\OneDrive\Área de Trabalho\analise_imigrantes\condominio.csv')
dados = pd.DataFrame(dados)
dados['Data'] = pd.to_datetime(dados['Data'])
dados['Ano'] = dados['Data'].dt.year
dados['Mês'] = dados['Data'].dt.month.map(meses)
dados['Categoria'] = dados['Histórico'].apply(lambda x: ' '.join(x.split()[:1]))


# Filtros 

st.sidebar.title('Filtros')

#anos = dados['Ano'].unique().tolist()
anos = ['Todos', 2021,2022,2023]
tipo_Conta = ['Todas','Contas Ordinária', 'Tarifas Públicas', 'Manutenção', 'Fundo de Reserva', 'Aluguel Cobertura','Fundo de Obras','Caixa Interno']

# Filtros interativos no st.sidebar

ano_selecionado = st.sidebar.selectbox('Selecione o ano', anos)

tipo_Conta_selecionada = st.sidebar._multiselect(
    'Tipo',dados['Tipo'].unique())
if tipo_Conta_selecionada:
    dados = dados[dados['Tipo'].isin(tipo_Conta_selecionada)]



dados_df = dados

# Aqui você pode utilizar os filtros para filtrar os dados e calcular os indicadores


if ano_selecionado == 'Todos':
    dados_df = dados[dados['Ano'].isin(anos[1:])]
    
else:
    dados_df = dados[dados['Ano'] == ano_selecionado]
   

#text = '' if ano_selecionado == 'Todos' else 'R$'


# Tabelas 
despesas_categoria = dados_df.groupby('Tipo')[['Valor']].sum()
despesas_categoria['R$'] = despesas_categoria['Valor']
despesas_categoria = despesas_categoria.sort_values('Valor')
despesas_categoria['R$'] = despesas_categoria['R$'].apply(format_numero)
despesas_categoria = despesas_categoria.reset_index()


despesas_periodo = dados_df.groupby('Mês')[['Valor']].sum().reset_index()
despesas_periodo['Ano'] = dados_df['Data'].dt.year
despesas_periodo['Mês'] = dados_df['Data'].dt.month.map(meses)
despesas_periodo['Mês_Numero'] = dados_df['Data'].dt.month
despesas_periodo = despesas_periodo.sort_values('Mês_Numero')
despesas_periodo['R$'] = despesas_periodo['Valor'].apply(format_numero)


despesas_mensais = dados_df.set_index('Data').groupby(
    pd.Grouper(freq='M'))['Valor'].sum().reset_index()
despesas_mensais['Ano'] = despesas_mensais['Data'].dt.year
despesas_mensais['Mês'] = despesas_mensais['Data'].dt.month.map(meses)
despesas_mensais['R$'] = despesas_mensais['Valor'].apply(format_numero)


years = [2021, 2022, 2023]

despesas_ano = dados_df.groupby('Ano')[['Valor']].sum().reset_index()
despesas_ano = despesas_ano[despesas_ano['Ano'].isin(years)]
despesas_ano['Delta'] = despesas_ano['Valor'].diff()
despesas_ano = despesas_ano.sort_values(by='Ano')
despesas_ano['Delta_Percentual'] = ((despesas_ano['Valor'] - despesas_ano['Valor'].shift(1)) / despesas_ano['Valor'].shift(1)) *100

#st.dataframe(despesas_ano)
if ano_selecionado == 'Todos':
    delta_2023 = despesas_ano.loc[despesas_ano['Ano'] == 2023,'Delta_Percentual'].values[0]
else:
    despesa_delta = dados.groupby('Ano')[['Valor']].sum().reset_index()
    #data_ano = [2021, 2022, 2023]
    despesa_delta = despesa_delta[despesa_delta['Ano'].isin(years)]
    despesa_delta['Delta'] = despesa_delta['Valor'].diff()
    despesa_delta = despesa_delta.sort_values(by='Ano')
    despesa_delta['Delta_Percentual'] = ((despesa_delta['Valor'] - despesa_delta['Valor'].shift(1)) / despesa_delta['Valor'].shift(1)) * 100
    delta_2023 = despesa_delta.loc[despesa_delta['Ano'] == ano_selecionado,'Delta_Percentual'].values[0]

top_despesas = dados_df.groupby('Categoria')[['Valor']].sum().reset_index()
top_despesas = top_despesas.sort_values('Valor',ascending=False)


'''despesas_2_anos = dados_df.set_index('Data').groupby(
    pd.Grouper(freq='M'))['Valor'].sum().reset_index()'''

despesas_2_anos = dados_df

#st.dataframe(delta_2023)

# Gráficos 
fig_despesas_ano = px.bar(despesas_ano,
                          x='Ano',
                          y='Valor',
                          text_auto= '.2s',
                          title='Total despeas por Ano')
fig_despesas_ano.update_traces(textfont_size=13, 
                               textangle=0, 
                               textposition="outside", 
                                cliponaxis=False,
                                marker_color="#FFC861"
                                )
fig_despesas_ano.update_yaxes(showticklabels=False)
fig_despesas_ano.update_xaxes(dtick='M12', tickformat='%Y')
fig_despesas_ano.update_layout(yaxis_title='',
                                     xaxis_title='',
                                     xaxis_tickangle=0,
                                     #width=600, 
                                     #height=400,
                                     yaxis_showgrid=False,
                                     #xaxis_tickformat = ".0f",  # Formato dos rótulos do eixo x (opcional)
                                     xaxis_showgrid=False,  # Exibir linhas de grade no eixo x (opcional)
                                     xaxis_gridcolor='lightgray',  # Cor das linhas de grade no eixo x (opcional)
                                     xaxis_gridwidth=0.5,
                                     font_family='Arial',
                                     font_size=22,                                     
                                     title_font_size=22,
                                     title_font_color="White",
                                     #colorway=["steelblue"],
                                     #margin=dict(l=50, r=50, t=50, b=50),  # Ajuste as margens do gráfico
                                     #plot_bgcolor="white",  # Defina a cor de fundo do gráfico
                                     #paper_bgcolor="white",  # Defina a cor de fundo do papel (área fora do gráfico)
                                     bargap=0.1,  # Ajuste o espaçamento entre as barras
                                     bargroupgap=0.1,  # Ajuste o espaçamento entre os grupos de barras
                                     )

fig_top_despesas = px.bar(top_despesas.head(),
                         x='Categoria',
                         y='Valor',
                         text_auto='.2s',
                         title='Top maiores despesas por Fornecedor'
                         )
fig_top_despesas.update_traces(textfont_size=13, 
                               textangle=0, 
                               textposition="outside", 
                                cliponaxis=False,
                                marker_color="#FFC861"
                                )
fig_top_despesas.update_yaxes(showticklabels=False)
fig_top_despesas.update_layout(yaxis_title='',
                                     xaxis_title='',
                                     xaxis_tickangle=0,
                                     #width=600, 
                                     #height=400,
                                     yaxis_showgrid=False,
                                     #xaxis_tickformat = ".0f",  # Formato dos rótulos do eixo x (opcional)
                                     xaxis_showgrid=False,  # Exibir linhas de grade no eixo x (opcional)
                                     xaxis_gridcolor='lightgray',  # Cor das linhas de grade no eixo x (opcional)
                                     xaxis_gridwidth=0.5,
                                     font_family='Arial',
                                     font_size=14,                                     
                                     title_font_size=22,
                                     title_font_color="White",
                                     #colorway=["steelblue"],
                                     #margin=dict(l=50, r=50, t=50, b=50),  # Ajuste as margens do gráfico
                                     #plot_bgcolor="white",  # Defina a cor de fundo do gráfico
                                     #paper_bgcolor="white",  # Defina a cor de fundo do papel (área fora do gráfico)
                                     bargap=0.1,  # Ajuste o espaçamento entre as barras
                                     bargroupgap=0.5,  # Ajuste o espaçamento entre os grupos de barras
                                     )
fig_despesas_categoria = px.bar(despesas_categoria,
                                orientation='h',
                                width=20,
                                x='Valor',
                                y='Tipo',                                
                                text_auto='.2s',
                                #color_discrete_sequence = px.colors.qualitative.Antique,
                                title= 'Despesas por tipo de Conta'             
                                )
fig_despesas_categoria.update_traces(
                                     textfont_size=13, 
                                     textangle=0, 
                                     textposition="outside", 
                                     cliponaxis=False,
                                     marker_color="#FFC861"
                                     )
fig_despesas_categoria.update_yaxes(showticklabels=True)

fig_despesas_categoria.update_xaxes(showticklabels=False)

fig_despesas_categoria.update_layout(yaxis_title='',
                                     xaxis_title='',
                                     xaxis_tickangle=0,
                                     #width=600, height=400,
                                     
                                     #xaxis_tickformat = ".0f",  # Formato dos rótulos do eixo x (opcional)
                                     xaxis_showgrid=False,  # Exibir linhas de grade no eixo x (opcional)
                                     xaxis_gridcolor='lightgray',  # Cor das linhas de grade no eixo x (opcional)
                                     #xaxis_gridwidth=0.5,
                                     font_family='Arial',
                                     font_size=14,                                     
                                     title_font_size=22,
                                     title_font_color="White",                                     
                                     #colorway=["steelblue"],
                                     margin=dict(l=50, r=10, t=120, b=40),  # Ajuste as margens do gráfico
                                     #plot_bgcolor="white",  # Defina a cor de fundo do gráfico
                                     #paper_bgcolor="white",  # Defina a cor de fundo do papel (área fora do gráfico)
                                     bargap=0.1,  # Ajuste o espaçamento entre as barras
                                     bargroupgap=0.1,  # Ajuste o espaçamento entre os grupos de barras
                                     )



color_map = {'setosa': '#FDC59B', 'versicolor': '#FDC5AF', 'virginica': '#FDC6BA'}

fig_despeas_mensais = px.line(despesas_mensais,
                               x='Mês',
                               y='Valor',
                               markers=True, 
                               color_discrete_map=color_map,                                                          
                               color='Ano',
                               line_dash='Ano',
                               title='Despesas mensais por Ano', 
                               
                                                                                                                        
                               )                              

fig_despeas_mensais.update_traces(textfont_size=13,
                                   line_shape='spline',
                                   #line_color="#F15F79",                                    
                                    #textposition="inside", 
                                    cliponaxis=True,
                                    marker_color="#FFA500",                                    
                                    line_width=3                              
                                     )
fig_despeas_mensais.update_yaxes(showticklabels=True)
fig_despeas_mensais.update_layout(#width=600, height=400,
                        yaxis_title='',
                        xaxis_title='',
                        font_family='Arial',
                        font_size=14,
                        font_color='grey',                       
                        title_font_color="White",                      
                        title_font_size=22,
                        xaxis_tickangle=-35,
                        #margin=dict(l=50, r=50, t=50, b=50),  # Ajuste as margens do gráfico
                        #plot_bgcolor="white",  # Defina a cor de fundo do gráfico
                        #paper_bgcolor="white",  # Defina a cor de fundo do papel (área fora do gráfico)
                        xaxis_showgrid=False,
                        yaxis_showgrid=False
                        )



# Visualização no streamlit

aba1, aba2 = st.tabs(['Dash', 'Despesas'])

with aba1:

    coluan1, coluna2 = st.columns(2)

    with coluan1:    
        st.metric('Despesas Total', format_numero(dados_df['Valor'].sum(),'R$'), delta=f"{delta_2023:.2f}",delta_color="inverse")
        st.plotly_chart(fig_despeas_mensais,use_container_width=True)
        st.plotly_chart(fig_top_despesas,use_container_width=True)    

    with coluna2: 
        
        st.metric('Quantidade de transações', format_numero(dados_df.shape[0]))    
        st.plotly_chart(fig_despesas_ano,use_container_width=True)   
        st.plotly_chart(fig_despesas_categoria,use_container_width=True)

with aba2:
    st.dataframe(despesas_2_anos)
   

    # tabela 
    



