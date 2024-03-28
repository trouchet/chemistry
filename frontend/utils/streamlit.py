import streamlit as st

def salvar_estado(nome:str, object: any):
    """
    Salva um objeto na sessão do Streamlit, associando-o a um nome específico.

    Args:
        nome (str): O nome que será usado para associar o objeto na sessão.
        objeto (any): O objeto que será salvo na sessão.

    Returns:
        None
    """

    if nome not in st.session_state:
        st.session_state[nome] = object
    return

def obter_estado(nome:str, opt=None):
    if opt is None:
        return st.session_state[nome]
      
    elif nome not in st.session_state:
        st.session_state[nome] = opt
    
    else:
        return st.session_state[nome]

