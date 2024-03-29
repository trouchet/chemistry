import pandas as pd
import streamlit as st
from os import path

from utils.streamlit import salvar_estado
from utils.dataframe import deletar_linha
from constants import FILENAME_PRODUTOS, \
    FILENAME_REGRAS 
from utils.dataframe import carregar_csv, \
    ajustar_colunas, \
    anexar_dataframe

################# Funções auxiliares ####################
@st.cache_data
def obter_itens_mais_vendidos(data_rootpath: str):
    filepath = path.join(data_rootpath, FILENAME_PRODUTOS)
    return carregar_csv(filepath)

def sugerir_items(
        lista: pd.DataFrame, 
        trends: pd.DataFrame,
        coluna_item: str, 
        max : int = 5
    ) -> pd.DataFrame:
    """
    Cria um DataFrame com as sugestões de compras baseado produtos da lista de compras
    """  
    if lista.empty:
        return None

    # sugestões de compras
    sugestoes = pd.DataFrame(columns=[coluna_item,"lift"])

    #Pegar todas as tendências
    for item in lista[coluna_item]:       
       # select all rows in Trends which value in column coluna_item matches item
       print(f"### item: {item} ")
       dados = trends[trends[coluna_item] == item]

       #Ordenar pelo Lift
       dados = dados.sort_values(by=["lift"], ascending=[False], inplace=False)
       
       #Remover correlações negativas
       dados = dados[dados["lift"] > 1.0]      
       if len(dados) > max:
           dados = dados.head(max)   
       
       drop_columns=[coluna_item, "zhangs_metric","aisle","department","vendidos"]
       dados = dados.drop(columns=drop_columns)
       dados.rename(columns={"Próximo":coluna_item}, inplace=True)
        
       # The code is unnecessarily complex and can be simplified
       # Create an empty DataFrame to store the final data
       final_data = pd.DataFrame(columns=[coluna_item,"lift"])
      
       # Iterate through each row in 'dados'
       for index, row in dados.iterrows():
            prod = row[coluna_item]
            lift = row["lift"]
            # Check if the product name contains '#'
            if "#" in prod:
                # Split the product name by '#' and iterate through each part
                for nm in prod.split("#"): 
                    # Check if the product is not already in 'final_data' and then append it
                    if nm not in final_data[coluna_item].values:
                        df2 = pd.DataFrame({coluna_item: [nm], "lift": [lift]})                          
                        final_data = anexar_dataframe(final_data, df2)

            # If the product name does not contain '#', check if it's not already in 'final_data' and then append it
            elif prod not in final_data[coluna_item].values:
                df2 = pd.DataFrame({coluna_item: [prod], "lift": [lift]})                              
                final_data = anexar_dataframe(final_data, df2)
       
       if not dados.empty:
           sugestoes = anexar_dataframe(sugestoes, final_data)

    # remover sugestões que já estão na lista
    for item in lista:  
        sugestoes = sugestoes[sugestoes[coluna_item] != item] 

    sugestoes.sort_values(by=["lift"], ascending=False, inplace=True)
    sugestoes.drop_duplicates(subset=coluna_item, inplace=True)
    
    return sugestoes

@st.cache_data
def sugestao_inicial(
    itens_mais_vendidos: pd.DataFrame,
    coluna_item: str, 
    top_=30, 
    n_itens=5, 
    lista_remover: pd.DataFrame = None
) -> pd.DataFrame:
    """
        Sugestão inicial para itens mais vendidos
    """
    sugestao = itens_mais_vendidos.head(top_)
    sugestao = sugestao.drop(columns=['product_id','vendidos'])
    sugestao.rename(columns={"product_name": coluna_item}, inplace=True)

    if lista_remover is not None:
        for item in lista_remover[coluna_item]:
            sugestao = deletar_linha(sugestao, coluna_item, item)

    sample = sugestao.sample(n=n_itens);    
    return sample

def obter_carrinho(
    coluna_item: str
)->pd.DataFrame:
    if 'carrinho' not in st.session_state:
        carrinho = pd.DataFrame(columns=[coluna_item])
        st.session_state['carrinho'] = carrinho        
    
    return st.session_state['carrinho']

def salvar_carrinho(
    carrinho: pd.DataFrame,
    coluna_item: str
):
    carrinho = carrinho.drop_duplicates(subset=[coluna_item])
    salvar_estado('carrinho', carrinho)
    return

def remover_item_no_carrinho(
        lista: pd.DataFrame,
        coluna_item: str
    ) -> pd.DataFrame:
    carrinho = obter_carrinho(coluna_item)
    for item in carrinho[coluna_item]:
        lista = deletar_linha(lista, coluna_item, item)
    return lista   

@st.cache_data
def obter_dados_de_vendas(
    data_rootpath: str
):
    filepath = path.join(data_rootpath, FILENAME_REGRAS)
    
    trends = carregar_csv(filepath)
    mais_vendidos = obter_itens_mais_vendidos(data_rootpath)
    
    # Remove colunas de baixo impacto
    trends_columns = [
        'ord','antecedent support',
        'consequent support', 'support',
        'confidence','leverage','conviction'
    ]
    trends = trends.drop(columns=trends_columns)
    
    # Ajusta nomes
    ajustar_colunas(trends, "antecedents")
    ajustar_colunas(trends, "consequents")

    trends = pd.merge(
        trends, mais_vendidos, 
        how="left", left_on="antecedents", right_on="product_name"
    )

    drop_cols = ['product_id','product_name',]
    trends = trends.drop(columns=drop_cols)
    
    rename_cols = {
        "antecedents": "Produto",
        "consequents": "Próximo"
    }
    trends.rename(columns=rename_cols, inplace=True)
    
    # Sorting
    trends.sort_values(
        by = ["Produto","lift"],
        ascending = [True,False], 
        inplace = True
    )

    return mais_vendidos, trends

