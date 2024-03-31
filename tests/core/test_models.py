# We will test the core functionality of the models
def test_recommendation_k_best_arbitrary(sv_recommender):
    order = ['apple', 'banana']
    expected_recommendation = ['orange', 'grape']
    
    sv_recommender._update_neighbors()
    recommendations = sv_recommender.recommend(order, method='k_best_arbitrary')
    
    assert isinstance(recommendations, list)
    assert len(recommendations) <= sv_recommender.n_suggestions
    assert all([isinstance(item, str) for item in recommendations])
    assert recommendations != order
    assert set(recommendations) == set(expected_recommendation)

def test_recommendation_k_best_random(sv_recommender):
    order = ['apple', 'banana']
    
    sv_recommender._update_neighbors()
    recommendations = sv_recommender.recommend(order, method='k_best_random')
    
    assert isinstance(recommendations, list)
    assert len(recommendations) <= sv_recommender.n_suggestions
    assert all([isinstance(item, str) for item in recommendations])
    assert recommendations != order
    
def test_recommendation_k_best_support(sv_recommender):
    order = ['apple', 'banana']
    
    sv_recommender._update_neighbors()
    recommendations = sv_recommender.recommend(order, method='k_best_support')
    
    assert isinstance(recommendations, list)
    assert len(recommendations) <= sv_recommender.n_suggestions
    assert all([isinstance(item, str) for item in recommendations])
    assert recommendations != order

def test_description(sv_recommender):
    item_ids = ['apple', 'banana']
    descriptions = sv_recommender.describe(item_ids)
    assert len(descriptions) == len(item_ids)
