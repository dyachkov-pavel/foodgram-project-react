from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import widgets
from .models import Recipe, Tag, RecipeIngredient, Ingredient
from django.http import request


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('full_name', 'username', 'email')


class IngredientQuantity(forms.ModelForm):
    model = RecipeIngredient
    fields = ['recipe', 'ingredient', 'quantity']


class RecipeForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(
        Tag.objects.all(), to_field_name='slug', widget=forms.CheckboxSelectMultiple)
    ingredient = forms.ModelMultipleChoiceField(
        Ingredient.objects.all(), to_field_name='title', required=False)

    class Meta:
        model = Recipe
        fields = ['title', 'tag', 'ingredient',
                  'time', 'description', 'image', ]
        labels = {'title': 'Название рецепта',
                  'tag': 'Тэги',
                  'ingredient': 'Ингредиенты',
                  'time': 'Время приготовления',
                  'description': 'Описание',
                  'image': 'Загрузить фото', }
