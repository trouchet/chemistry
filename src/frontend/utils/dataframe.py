import pandas as pd
import streamlit as st

@st.cache_data
def carregar_csv(filename:str)->pd.DataFrame:
    """
    Carrega arquivos CSV
    """
    print("Carregando arquivo de dados : " + filename)
    return pd.read_csv(filename)

def ajustar_colunas(
        df : pd.DataFrame, 
        coluna:str
)->pd.DataFrame:
    """
    Adjust column for string instead of frozen set
    """
    column_data = df[coluna]
    novos_dados = []

    # Desemble frozenset
    for item in column_data:
        if isinstance(item, str):
            novo_item = item.replace("frozenset({'","")\
                         .replace("'})","")
            novo_item = novo_item.replace("', '","#")

        elif isinstance(item, set):
            agrega = ""
            primeiro = True
            for subitem in item:
                agrega += subitem if primeiro else ("#" + subitem)
                primeiro = False

            novo_item = agrega

        novos_dados.append(novo_item)

    df[coluna] = novos_dados
    return df

def obter_dataframe_com_selecoes(
        df:pd.DataFrame, 
        key="Chave", title="Selecione", sidebar=True, selecionados=False
    ):
    df_with_selections = df.copy()
    df_with_selections.insert(0, title, selecionados)    
    
    # Obter seleções do usuário com st.data_editor
    column_config={title: st.column_config.CheckboxColumn(required=True)}
    
    if sidebar:
        edited_df = st.sidebar.data_editor(
            df_with_selections,
            hide_index=True,
            column_config=column_config,
            disabled=df.columns,
            key = key + "_Side",
        )
    else:
        edited_df = st.data_editor(
            df_with_selections,
            hide_index=True, 
            column_config=column_config,
            disabled=df.columns, 
            key = key + "_MAIN",
        )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df[title]]
    return selected_rows.drop(title, axis=1)

def anexar_dataframe(
        s1: pd.DataFrame, 
        s2: pd.DataFrame, 
        force = False
    ) -> pd.DataFrame:
    """
    Anexa um DataFrame a outro
    """
    if not force:
        return pd.concat([s1,s2], ignore_index=True)

    for i, _ in s2.iterrows():   
        print(f"i = {i}")         
        row_dict = s2.iloc[i].to_dict()               
        s1.loc[len(s1)] = row_dict
    
    return s1 

def deletar_linha(
        lista: pd.DataFrame, 
        coluna:str, 
        valor: any
    ) -> pd.DataFrame:
    lista = lista[lista[coluna]!=valor]
    return lista

def adicionar_item_a_lista(
        lista: list, 
        item: pd.DataFrame
    ) -> pd.DataFrame:
    """
    Adiciona um novo item na lista.
    Retorna a lista
    """    
    print(f"## Adicionando {item}")
    if len(item) == 0 or item.empty:
        return lista     
        
    lista = anexar_dataframe(lista, item)
    if "lift" in lista.columns:
        lista = lista.drop(columns={"lift"})
    
    lista = lista.drop_duplicates(subset=['Produto'])
    return lista
