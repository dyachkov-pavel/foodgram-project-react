from django import forms
from django.core.exceptions import ValidationError
from .models import Recipe, Tag, RecipeIngredient, Ingredient
from django.shortcuts import get_object_or_404


class IngredientsError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class RecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    tag = forms.ModelMultipleChoiceField(
        Tag.objects.all(),
        to_field_name='slug',
        widget=forms.CheckboxSelectMultiple
    )
    ingredient = forms.ModelMultipleChoiceField(
        Ingredient.objects.all(),
        to_field_name='title',
        required=False
    )

    class Meta:
        model = Recipe
        fields = ['title',
                  'tag',
                  'ingredient',
                  'time',
                  'description',
                  'image', ]
        labels = {'title': 'Название рецепта',
                  'tag': 'Тэги',
                  'ingredient': 'Ингредиенты',
                  'time': 'Время приготовления',
                  'description': 'Описание',
                  'image': 'Загрузить фото', }

    def get_ingredients(self):
        ingredients = []
        for string in self.request.POST:
            if 'nameIngredient_' in string:
                ingredients.append(self.request.POST.get(string))
        return ingredients

    def get_quantity(self):
        quantity = []
        for string in self.request.POST:
            if 'valueIngredient_' in string:
                quantity.append(self.request.POST.get(string))
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        ingredients = self.get_ingredients()
        quantity = self.get_quantity()
        ingredients_len = len(ingredients)
        quantity_len = len(quantity)
        if ingredients_len != quantity_len or not ingredients:
            self.add_error(
                'ingredient',
                'Не забудьте добавить ингредиенты'
            )
        if '0' in quantity:
            self.add_error(
                'ingredient',
                'Проверьте, чтобы количество каждого '
                'ингредиента было больше нуля'
            )

    def save(self):
        ingredients = self.get_ingredients()
        quantity = self.get_quantity()
        self.instance = super().save(commit=False)
        self.instance.save()
        self.save_m2m()
        for index, ingredient in enumerate(ingredients):
            used_ingredient = get_object_or_404(
                Ingredient,
                title=ingredient
            )
            ing_in_recipe = RecipeIngredient.objects.filter(
                recipe=self.instance,
                ingredient=used_ingredient,
            )
            if ing_in_recipe.exists():
                ingredient_in_recipe = ing_in_recipe[0]
                ingredient_in_recipe.quantity += int(quantity[index])
                ingredient_in_recipe.save()
            else:
                RecipeIngredient.objects.create(
                    recipe=self.instance,
                    ingredient=used_ingredient,
                    quantity=quantity[index]
                )
        return self.instance
