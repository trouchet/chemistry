import pytest

from src.core.recommendation.models import \
    SVRecommender, \
    Basket, \
    Product, \
    product_to_basket

# We will test the core functionality of the models
def test_basket_validity():
    basket = Basket(
        company_id='acme',
        items=['apple', 'banana'], 
        age_months=42
    )
    
    assert basket.is_age_valid() == False

def test_product_to_basket():
    company_id_ = 'acme'
    product = Product(company_id=company_id_, id='apple')
    basket = product_to_basket(product)
    expected_basket = Basket(company_id=company_id_, items=['apple'])

    assert set(basket.items) == set(expected_basket.items)

def test_recommendation_k_best_arbitrary(sv_recommender):
    order = ['apple', 'banana']
    expected_recommendation = ['orange', 'grape']
    
    sv_recommender._update_neighbors()
    recommendations = sv_recommender.recommend(order, method='arbitrary')

    assert isinstance(recommendations, list)
    assert len(recommendations) <= sv_recommender.n_suggestions
    assert all([isinstance(item, str) for item in recommendations])
    assert recommendations != order
    assert set(recommendations) == set(expected_recommendation)

def test_recommendation_k_best_random(sv_recommender):
    order = ['apple', 'banana']
    
    sv_recommender._update_neighbors()
    recommendations = sv_recommender.recommend(order, method='random')
    
    assert isinstance(recommendations, list)
    assert len(recommendations) <= sv_recommender.n_suggestions
    assert all([isinstance(item, str) for item in recommendations])
    assert recommendations != order
    
def test_recommendation_k_best_support(sv_recommender):
    order = ['apple', 'banana']
    
    sv_recommender._update_neighbors()
    recommendations = sv_recommender.recommend(order, method='support')
    
    assert isinstance(recommendations, list)
    assert len(recommendations) <= sv_recommender.n_suggestions
    assert all([isinstance(item, str) for item in recommendations])
    assert recommendations != order

def test_get_sv_recommender_invalid_suggestion_count(recommendation_dataframe):
    with pytest.raises(ValueError) as exc_info:
        SVRecommender(recommendation_dataframe, 
            'order_id', 'item_id', 'description',
            n_suggestions=-1, n_best_neighbors=-1
        )

def test_get_sv_recommender_invalid_method(sv_recommender):
    with pytest.raises(ValueError) as exc_info:
        sv_recommender._update_neighbors()
        sv_recommender.recommend(['apple', 'banana'], method='invalid_method')

def test_description(sv_recommender):
    item_ids = ['apple', 'banana']
    descriptions = sv_recommender.describe(item_ids)

    assert len(descriptions) == len(item_ids)
    assert descriptions == ['Description of apple', 'Description of banana']

def test_get_sv_recommender_invalid_item(sv_recommender):
    sv_recommender._update_neighbors()
    descriptions = sv_recommender.describe(['dragon fruit', 'banana'])

    assert descriptions == ['', 'Description of banana']
