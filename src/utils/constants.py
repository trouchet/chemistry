# Descrição: Constantes usadas nas funções utilitárias da aplicação.
from fastapi import status

# Nível de confiança para listas em histogramas
PLOT_CONFIDENCE = 0.99

# Códigos de status HTTP
OK_200 = status.HTTP_200_OK
CREATED_201 = status.HTTP_201_CREATED
BAD_REQUEST_400 = status.HTTP_400_BAD_REQUEST
INTERNAL_SERVER_ERROR_500 = status.HTTP_500_INTERNAL_SERVER_ERROR

# Média de itens por conjunto de itens
MEAN_ITEMS_PER_ITEMSET = 5

# Tamanho padrão do token
DEFAULT_TOKEN_LENGTH = 10

# Colunas do conjunto de dados
# NOTE: This is a hardcode list of columns
# TODO: Make this dynamic
dataset_columns = [
    'itemset_timestamp', 
    'itemset_id', 
    'agent_id', 
    'item_id', 
    'item_description', 
    'item_quantity', 
    'item_value'
]