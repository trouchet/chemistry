import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt

def obter_regras_apriori(
	dados_treino: pd.DataFrame, 
	min_support_ = 0.001, 
	min_threshold_ = 0.05
) -> pd.DataFrame:
    """
    Apply the Apriori algorithm to analyze association rules.

    Parameters
    ----------
    basket : pd.DataFrame
        The input DataFrame containing transaction data.
    min_support_ : float, optional
        The minimum support threshold for generating frequent itemsets. Default is 0.001.
    min_threshold_ : float, optional
        The minimum threshold for generating association rules. Default is 0.05.

    Returns
    -------
    pd.DataFrame
        The DataFrame containing the generated association rules.

    """
    # Transformar dados para o formato adequado
    te = TransactionEncoder()
    te_ary = te.fit(dados_treino).transform(dados_treino)
    dados_treino_df = pd.DataFrame(te_ary, columns=te.columns_)
    
    # Aplicar o Algoritmo Apriori    
    itemsets_frequentes = apriori(
        dados_treino_df, 
        min_support=min_support_, 
        use_colnames=True
    )
    
    # Gerar Regras de Associação    
    regras = association_rules(
        itemsets_frequentes, 
        metric="confidence", 
        min_threshold=min_threshold_
    )
    
    return regras


def preparar_dados(
	basket_raw_: pd.DataFrame, 
    principal_: str = "order_id", 
	eixo_: str = "product_name", 
	allow_duplicate_on_axs_:bool = False, 
	print_info_: bool=True
) -> pd.DataFrame:
    """
    Prepare data for the specified axis.
    
    Parameters
    ----------
    basket_raw_ : pd.DataFrame
        The input DataFrame containing transaction data.
    principal_ : str, optional
        The axis to group by
    eixo_ : str, optional
        The axis for which the data is being prepared. Default is "product_name".
    
    Returns
    -------
    pd.DataFrame
        The prepared DataFrame.
    """
    print("Preparando dados para Eixo: " + eixo_)
    
    # Preparar os Dados
    # Agrupar produtos por 'principal_' e criar uma lista de produtos para cada pedido
    basket = None
    if not allow_duplicate_on_axs_:
         basket = basket_raw_.groupby(principal_)[eixo_].apply(lambda x: list(set(x)))
    else:
         basket = basket_raw_.groupby(principal_)[eixo_].apply(list) 
    
    if print_info_:
         imprime_dataframe_stats(pd.DataFrame(basket), "Basket " + eixo_)
    
    return pd.DataFrame(basket)

def imprime_painel(regras, info):
    print("Charts " + info)

    # Criando um gráfico de dispersão para suporte vs confiança
    plt.scatter(regras['support'], regras['confidence'], alpha=0.5)
    plt.title('Regras de Associação: Suporte vs Confiança ' + info)
    plt.xlabel('Suporte')
    plt.ylabel('Confiança')
    plt.show()

    # Criando um gráfico de dispersão para suporte vs lift
    plt.scatter(regras['support'], regras['lift'], alpha=0.5)
    plt.title('Regras de Associação: Suporte vs Lift ' + info)
    plt.xlabel('Suporte')
    plt.ylabel('Lift')
    plt.show()

    # Criando um gráfico de dispersão para confiança vs lift
    plt.scatter(regras['confidence'], regras['lift'], alpha=0.5)
    plt.title('Regras de Associação: Confiança vs Lift' + info)
    plt.xlabel('Confiança')
    plt.ylabel('Lift')
    plt.show()

def imprime_dataframe_stats(
	data: pd.DataFrame, 
	descricao: str = "DataFrame"
):
    """
    Print básico dos dados
    """
    print("\n=======================")  
    print(descricao)

    print(f"Colunas: {data.columns}") 
    print(f"Linhas: {len(data)}")

    print("Top 10")
    print(data.head(10))  

print("##########################################################")
print("##########################################################")

from os import getcwd, path

# 1. Importar os Dados
# Substitua pelo caminho real do seu arquivo CSV
dataset_filename = "market_01.csv"
caminho_arquivo_dados = path.join(getcwd(), dataset_filename)
dados_brutos = pd.read_csv(caminho_arquivo_dados, encoding='utf-8', compression=None)

dados = dados_brutos[
    dados_brutos["department"].isin(["produce","dairy eggs"])
]

print(f"Dados Brutos \n Colunas: {dados.columns} \n Linhas: {len(dados)}")
print("=================================================================")

eixo = "product_name"

# 1. Filtrar dadosc
imprime_dataframe_stats(dados, "Dados da Manhã")

# 2. Preparar os Dados
# Agrupar produtos por 'order_id' e criar uma lista de produtos para cada pedido
cesta_ = dados.groupby('order_id')[eixo].apply(list)
imprime_dataframe_stats(pd.DataFrame(cesta_), "Cesta")

# 3. Aplicar o Algoritmo Apriori
print("\n Analise Apriori - Aguarde ...")
print("================================")
regras_ = obter_regras_apriori(cesta_, min_support_=0.003, min_threshold_=0.01)
imprime_dataframe_stats(regras_, "Analise - Manhã")

# 4. Salvar os Resultados
filename = path.join(getcwd(), 'Apriori_Regras_Manha.csv')
regras_.to_csv(filename, index=True)

print("That's all!")
