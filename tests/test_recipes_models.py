from datetime import timedelta

import pytest

from recipes.models import Rating, Recipe


def test_basic_recipe_model():
    recipe = Recipe(
        name='Scrambled Eggs',
        prep_time=timedelta(minutes=10),
        difficulty=1,
        vegetarian=True,
    )

    assert recipe.name == 'Scrambled Eggs'
    assert recipe.prep_time == timedelta(minutes=10)
    assert recipe.difficulty == 1
    assert recipe.vegetarian is True


def test_fail_recipe_invalid_prep_time():
    with pytest.raises(ValueError):
        Recipe(
            name='Scrambled Eggs',
            prep_time=timedelta(minutes=-10),  # invalid
            difficulty=1,
            vegetarian=True,
        )


def test_fail_recipe_invalid_difficulty():
    with pytest.raises(ValueError):
        Recipe(
            name='Scrambled Eggs',
            prep_time=timedelta(minutes=-10),
            difficulty=5,  # invalid
            vegetarian=True,
        )


def test_basic_rating(recipe):
    rating = Rating(recipe=recipe, value=5)

    assert rating.recipe == recipe
    assert rating.value == 5


def test_fail_invalid_rating_value(recipe):
    with pytest.raises(ValueError):
        Rating(
            recipe=recipe,
            value=0,
        )

    with pytest.raises(ValueError):
        Rating(
            recipe=recipe,
            value=6,
        )
