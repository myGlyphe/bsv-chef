import pytest
from unittest.mock import MagicMock

from src.controllers.recipecontroller import RecipeController
from src.util.dao import DAO
from src.static.diets import Diet

recipes = [
    {'name': 'First', 'diets': ['vegan'], 'ingredients': {'a': 1, 'b': 2, 'c': 3}},
    {'name': 'Second', 'diets': ['vegetarian', 'normal'], 'ingredients': {'x': 10, 'y': 20, 'z': 30}},
]

# add your test case implementation here
@pytest.fixture
def get_controller():
    mockedDAO = MagicMock(spec=DAO)
    controller = RecipeController(items_dao=mockedDAO)
    controller.recipes = recipes
    return controller

@pytest.mark.unit
def test_get_recipe_take_best_true(get_controller):
    get_controller.get_readiness_of_recipes = MagicMock(return_value={'First': 0.9, 'Second': 0.8})
    result = get_controller.get_recipe(Diet.VEGAN, True)
    assert result in ['First', 'Second']
    
@pytest.mark.unit
def test_get_recipe_take_best_false(get_controller):
    get_controller.get_readiness_of_recipes = MagicMock(return_value={'First': 0.9, 'Second': 0.8})
    result = get_controller.get_recipe(Diet.VEGAN, False)
    assert result == 'First'

@pytest.mark.unit
def test_get_recipe_single_recipe(get_controller):
    get_controller.get_readiness_of_recipes = MagicMock(return_value={'First': 0.9})
    result = get_controller.get_recipe(Diet.VEGAN, True)
    assert result == 'First'

@pytest.mark.unit
def test_get_recipe_all_below_threshold(get_controller):
    get_controller.get_readiness_of_recipes = MagicMock(return_value={'First': 0.05, 'Second': 0.04})
    result = get_controller.get_recipe(Diet.VEGAN, True)
    assert result is None

@pytest.mark.unit
def test_get_recipe_no_valid_recipe_for_diet(get_controller):
    get_controller.get_readiness_of_recipes = MagicMock(return_value={'First': 0.9})
    result = get_controller.get_recipe(Diet.VEGAN, True)
    assert result == 'First'

@pytest.mark.unit
def test_get_recipe_valid_for_another_diet(get_controller):
    get_controller.get_readiness_of_recipes = MagicMock(return_value={'Second': 0.8})
    result = get_controller.get_recipe(Diet.VEGETARIAN, True)
    assert result == 'Second'

@pytest.mark.unit
def test_get_recipe_no_recipes(get_controller):
    get_controller.recipes = []
    get_controller.get_readiness_of_recipes = MagicMock(return_value={})
    result = get_controller.get_recipe(Diet.VEGAN, True)
    assert result is None
    
@pytest.mark.unit
def test_get_recipe_multiple_same_readiness(get_controller):
    get_controller.get_readiness_of_recipes = MagicMock(return_value={'First': 0.9, 'Second': 0.9})
    result = get_controller.get_recipe(Diet.VEGAN, True)
    assert result in ['First', 'Second']

@pytest.mark.unit
def test_get_recipe_multiple_diets(get_controller):
    get_controller.get_readiness_of_recipes = MagicMock(return_value={'First': 0.9, 'Second': 0.8})
    result = get_controller.get_recipe(Diet.NORMAL, True)
    assert result == 'Second'

@pytest.mark.unit
def test_get_recipe_no_recipes_for_diet(get_controller):
    get_controller.get_readiness_of_recipes = MagicMock(return_value={})
    result = get_controller.get_recipe(Diet.VEGAN, True)
    assert result is None
    

if __name__ == "__main__":
    pytest.main()