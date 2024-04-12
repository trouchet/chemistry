# Description: Constants for recommendation module

# Default number of suggestions
N_SUGGESTIONS_DEFAULT = 6

# Default number of best neighbors
N_BEST_NEIGHBORS_DEFAULT = 3

# Available association metrics
AVAILABLE_METRICS = ['support', 'confidence', 'lift', 'leverage', 'conviction']

# Available recommendation algorithms
AVAILABLE_METHODS = ['arbitrary', 'random'] + AVAILABLE_METRICS

# Default recommendation algorithm
RECOMMENDATION_ALGO_DEFAULT = 'support'

# Default minimum support and threshold
DEFAULT_MIN_SUPPORT = 0.001
DEFAULT_MIN_THRESHOLD = 0.05

# Confidence level for sets
MIN_SET_SIZE_CONFIDENCE = 0.95

# Mean number of items per itemsets
MEAN_ITEMS_PER_ITEMSET = 5
