import pandas as pd

from core.recommendation.extract_transform import get_sets_count_per_items_dict
from utils.dataframe import get_unique_elements

def get_items_support(
    sets_count_dict: dict, 
    sets_total: int
):
    return {
        item_id: sets_count/sets_total
        for item_id, sets_count in sets_count_dict.items()
    }

# Confidence(A→B) = Probability(A & B) / Support(A)
def get_items_confidence(
    item_to_neighbors_dict: dict,
    items_support_dict: dict,
    sets_total: int
):    
    
    neighbors_support_dict = {
        item_id: {
            neighbor_id: neighbor_count/sets_total
            for neighbor_id, neighbor_count in neighbors.items()
        }
        for item_id, neighbors in item_to_neighbors_dict.items()
    }
    
    return {
        item_id: {
            neighbor_id: neighbor_support/items_support_dict[item_id]
            for neighbor_id, neighbor_support in neighbors.items()
        }
        for item_id, neighbors in neighbors_support_dict.items()
    }

# Lift(A→B) = Confidence(A→B) / Support(B)
def get_items_lift(
    items_supports_dict: dict, 
    confidences_dict: dict
):
    return {
        item_id: {
            neighbor_id: neighbor_confidence/items_supports_dict[neighbor_id]
            for neighbor_id, neighbor_confidence in this_item_confidences.items()
        }
        for item_id, this_item_confidences in confidences_dict.items()
    }

def get_association_metrics(
    df_: pd.DataFrame,
    neighbors: dict,
    sets_column: str, 
    items_column: str
):
    sets_count_dict = get_sets_count_per_items_dict(df_, sets_column, items_column)
    sets_total = len(get_unique_elements(df_, sets_column))
    
    items_support = get_items_support(sets_count_dict, sets_total)
    items_confidence = get_items_confidence(neighbors, items_support, sets_total)
    items_lift = get_items_lift(items_support, items_confidence)

    # TODO: 
    # Leverage: P(A and B) - P(A) * P(B)
    # Conviction: P(A and B) / (P(A) * P(B))
    # zhang_metric: Zhang(A -> B) = P(B_given_A) - P(B)

    return {
        item_id: {
            'support': item_support,
            'neighbors': {
                neighbor_id: {
                    'confidence': neighbor_confidence,
                    'lift': items_lift[item_id][neighbor_id]
                } 
                for neighbor_id, neighbor_confidence in items_confidence[item_id].items()
            }
        }
        for item_id, item_support in items_support.items()
    }