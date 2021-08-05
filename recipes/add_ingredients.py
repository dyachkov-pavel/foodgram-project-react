from django.http import request
from .models import Ingredient, Recipe, RecipeIngredient


def add_ingredients(request, recipe):
    print(request.POST)
    ingredients = []
    quantity = []
    for string in request.POST:
        if 'nameIngredient_' in string:
            ingredients.append(request.POST.get(string))
        if 'valueIngredient_' in string:
            quantity.append(request.POST.get(string))
    if len(ingredients) == len(quantity):
        for i in range(len(ingredients)):
            used_ingredient = Ingredient.objects.get(title=ingredients[i])
            RecipeIngredient.objects.create(
                recipe=recipe, 
                ingredient=used_ingredient, 
                quantity=quantity[i]
            )
