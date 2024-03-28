####################################################################
# Bibliotecas
####################################################################

import streamlit as st
from st_aggrid import AgGrid
from warnings import simplefilter
from os import path

from core import obter_dados_de_vendas, \
            obter_carrinho, \
            salvar_carrinho, \
            sugestao_inicial, \
            sugerir_items, \
            remover_item_no_carrinho

from constants import DEFAULT_ITEM_COUNT

from utils.dataframe import obter_dataframe_com_selecoes, \
    adicionar_item_a_lista

####################################################################
# Configuração
####################################################################

# Suppress FutureWarning messages
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=DeprecationWarning)

###################### Carregamento de dados #####################
data_rootpath = path.dirname(__file__) 
itens_mais_vendidos, trends = obter_dados_de_vendas(data_rootpath)

###################### Interface do Usuário ######################

st.write("# Suas Vendas ")
st.write("## Adivinhando o próximo Item: ")

# Botão que limpa o estado do aplicativo
if st.sidebar.button('Reboot'):
    st.session_state.resultado = None
    st.cache_data.clear()
    st.sidebar.write('O estado do aplicativo foi limpo.')

# Define widget para quantidade de entradas vendidas
user_input = st.number_input(
    'Inserir o número de items no display:', 
    min_value=DEFAULT_ITEM_COUNT, max_value=len(itens_mais_vendidos)
)

amostra_msg = f"#### Vendas (amostra de {user_input} itens mais vendidos)"
st.write(amostra_msg)   

AgGrid(
    itens_mais_vendidos.head(user_input), 
    height=300 , width=1600, fit_columns_on_grid_load=True
)

with st.expander("Métricas de associação", expanded=False):
    lift_definition = 'Probabilidade de itens serem levados juntos. Valor maior que 1 indica maior possibilidade e menor do 1 indicam aversão'
    zhang_definition = 'Idem acima. Valor próximo à 1.0 indicam alta probabilidade e valores abaixo de 0.0 indicam aversão.'
    st.write(
        """<p>Indicadores:</p>
            <li>Lift: {lift_definition}</li>
            <li>Zhang's Metric: {zhang_definition}</li>
        """.format(lift_definition=lift_definition, zhang_definition=zhang_definition),
        unsafe_allow_html=True
    )

    AgGrid(trends, height=300, fit_columns_on_grid_load=True)

###### Carrinho de Compras
coluna_item = "Produto"

items_atuais = obter_carrinho(coluna_item)

st.write("#### Carrinho de Compras")
st.sidebar.write("Produtos mais vendidos: ")
sugestao_mais_vendidos = sugestao_inicial(
    itens_mais_vendidos, coluna_item, 
    top_=15, n_itens=10
)

selection = obter_dataframe_com_selecoes(
    sugestao_mais_vendidos, 
    key="Mais_vendidos"
)

carrinho = adicionar_item_a_lista(items_atuais, item=selection) 
salvar_carrinho(carrinho, coluna_item)

if not carrinho.empty:
    st.sidebar.write("Leve também: ")
    sugestoes = sugerir_items(
        lista=carrinho, 
        trends=trends,
        coluna_item=coluna_item
    )
    
    sugestoes = remover_item_no_carrinho(sugestoes, coluna_item)
    item_novo = obter_dataframe_com_selecoes(sugestoes, key="Sugestões")
    carrinho = adicionar_item_a_lista(carrinho, item=item_novo)      
    
    salvar_carrinho(carrinho, coluna_item)
    print(f"# Carrinho: {carrinho}")

if carrinho is not None:
    st.write("Meu Carrinho final de Compras:")
    AgGrid(carrinho, height=250)




 

