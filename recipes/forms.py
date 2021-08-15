from django import forms
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

    def save(self, commit=True):
        self.instance = super().save(commit=False)
        if commit:
            self.instance.save()
            self.save_m2m()
            ingredients = []
            quantity = []
            for string in self.request.POST:
                if 'nameIngredient_' in string:
                    ingredients.append(self.request.POST.get(string))
                if 'valueIngredient_' in string:
                    quantity.append(self.request.POST.get(string))
            ingredients_len = len(ingredients)
            quantity_len = len(quantity)
            if ingredients_len == quantity_len and ingredients_len != 0:
                for ingredient in enumerate(ingredients):
                    used_ingredient = get_object_or_404(
                        Ingredient,
                        title=ingredient[1]
                    )
                    RecipeIngredient.objects.create(
                        recipe=self.instance,
                        ingredient=used_ingredient,
                        quantity=quantity[ingredient[0]]
                    )
            else:
                raise IngredientsError(
                    'No ingredietns were provided or ingredients and its quantity do not match'
                )
        return self.instance
