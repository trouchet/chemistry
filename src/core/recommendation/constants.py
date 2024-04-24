# Descrição: Constantes para o módulo de recomendação

# Número padrão de sugestões
N_SUGGESTIONS_DEFAULT = 6

# Número padrão dos melhores vizinhos
N_BEST_NEIGHBORS_DEFAULT = 3

# Métricas de associação disponíveis
AVAILABLE_METRICS = ['support', 'confidence', 'lift', 'leverage', 'conviction']

# Algoritmos de recomendação disponíveis
AVAILABLE_METHODS = ['arbitrary', 'random'] + AVAILABLE_METRICS

# Algoritmo de recomendação padrão
RECOMMENDATION_ALGO_DEFAULT = 'support'

# Suporte mínimo padrão e limiar
DEFAULT_MIN_SUPPORT = 0.001
DEFAULT_MIN_THRESHOLD = 0.05

# Nível de confiança para conjuntos
MIN_SET_SIZE_CONFIDENCE = 0.95

# Média do número de itens por itemset
MEAN_ITEMS_PER_ITEMSET = 5
