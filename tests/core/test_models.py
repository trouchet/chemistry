import pytest

from src.core.recommendation.models import (
    SVRecommender,
    Product,
    product_to_basket,
    Basket,
)

from src.core.recommendation.metrics import (
    get_items_support,
    get_items_neighbors_support,
    get_items_confidence,
    get_items_lift,
    get_association_metrics,
    get_neighbor_association_metrics,
)

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
    with pytest.raises(ValueError):
        SVRecommender(
            recommendation_dataframe,
            'order_id',
            'item_id',
            'description',
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
    with pytest.raises(ValueError):
        sv_recommender._update_neighbors()
        sv_recommender.recommend(['apple', 'banana'], method='invalid_method')


def test_description(sv_recommender):
    item_ids = ['apple', 'banana']
    descriptions = sv_recommender.describe(item_ids)

    assert len(descriptions) == len(item_ids)
    assert descriptions == ['Description of apple', 'Description of banana']


def test_get_sv_recommender_invalid_item(sv_recommender):
    descriptions = sv_recommender.describe(['dragon fruit', 'banana'])

    assert descriptions == ['', 'Description of banana']
