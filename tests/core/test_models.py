import pytest

from src.core.recommendation.models import (
    SVRecommender,
    Product,
    product_to_basket,
    Basket,
)

from src.core.recommendation.constants import AVAILABLE_METHODS as AVA
from src.core.recommendation.metrics import get_association_metrics

# We will test the core functionality of the models
def test_basket_validity():
    basket = Basket(company_id='acme', items=['apple', 'banana'], age_months=42)

    assert not basket.is_age_valid()


def test_basket_eq(sample_basket_factory):
    basket_1 = sample_basket_factory(['apple', 'banana'])
    basket_2 = sample_basket_factory(['apple', 'banana'])

    assert basket_1 == basket_2


def test_basket_ne(sample_basket_factory):
    basket_1 = sample_basket_factory(['apple', 'banana'])
    basket_2 = sample_basket_factory(['apple', 'orange'])

    assert basket_1 != basket_2


def test_basket_repr(sample_basket_factory):
    basket = sample_basket_factory(['apple', 'banana'])

    assert repr(basket) == "Basket(company_id=acme, items=['apple', 'banana'])"

    many_items = [
        'apple',
        'banana',
        'orange',
        'grape',
        'kiwi',
        'pear',
        'peach',
        'plum',
        'mango',
        'papaya',
        'pineapple',
        'dragon fruit',
    ]
    basket = sample_basket_factory(many_items)

    summarized_items = "['apple', 'banana', 'orange', 'grape', 'kiwi', 'pear', ...]"
    assert repr(basket) == f"Basket(company_id=acme, items={summarized_items})"


def test_basket_eq_different_type(sample_basket_factory):
    basket = sample_basket_factory(['apple', 'banana'])

    assert basket != 'apple'


def test_item_description(sample_item):
    assert sample_item.description == 'Description of apple'


def test_item_repr(sample_item):
    assert repr(sample_item) == 'Item(identifier=apple, value=0.5)'


def test_product_to_basket():
    company_id_ = 'acme'
    product = Product(
        company_id=company_id_, 
        product_id='apple'
    )
    basket = product_to_basket(product)
    expected_basket = Basket(company_id=company_id_, items=['apple'])

    assert set(basket.items) == set(expected_basket.items)

@pytest.mark.parametrize("method", AVA)
def test_recommendation_k_best_arbitrary(sv_recommender, method):
    order = ['apple', 'banana']

    sv_recommender._update_neighbors()
    recommendations = sv_recommender.recommend(order, method=method)

    assert isinstance(recommendations, list)
    assert len(recommendations) <= sv_recommender.n_suggestions
    assert all([isinstance(item, str) for item in recommendations])
    assert recommendations != order

def test_get_sv_recommender_invalid_suggestion_count(recommendation_dataframe):
    with pytest.raises(ValueError):
        SVRecommender(
            recommendation_dataframe,
            'order_id',
            'item_id',
            'item_description',
            n_suggestions=-1,
            n_best_neighbors=-1,
        )

def test_get_sv_recommender_metrics(sample_sets_info: dict):
    df = sample_sets_info["dataframe"]
    set_column = sample_sets_info["set_column"]
    item_column = sample_sets_info["item_column"]
    sets_neighbors_dict = sample_sets_info["neighbors"]
    expected_metrics = sample_sets_info["expected_metrics"]

    dataframe_metrics = get_association_metrics(
        df, sets_neighbors_dict, set_column, item_column
    )

    assert dataframe_metrics == expected_metrics

def test_get_sv_recommender_invalid_method(sv_recommender):
    order = ['apple', 'banana']

    with pytest.raises(ValueError):
        sv_recommender.recommend(order, 'invalid_method')


def test_description(sv_recommender, small_sample_items, small_sample_description):
    descriptions = sv_recommender.describe(small_sample_items)

    assert len(descriptions) == len(small_sample_items)
    assert descriptions == small_sample_description


def test_get_sv_recommender_invalid_item(
    sv_recommender,
    small_sample_items,
    small_sample_description
):
    descriptions = sv_recommender.describe(small_sample_items)

    assert descriptions == small_sample_description 
