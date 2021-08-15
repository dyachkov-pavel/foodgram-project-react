from django import template
from django.contrib.auth import get_user_model
from django.http import request
from rest_framework.generics import get_object_or_404


User = get_user_model()

register = template.Library()


@register.filter
def tag_filter(request, chosen_tag):
    original_request = request.GET.copy()
    tags_list = request.GET.getlist('tags')
    if chosen_tag.slug in tags_list:
        tags_list.remove(chosen_tag.slug)
        original_request.setlist('tags', tags_list)
    else:
        original_request.appendlist('tags', chosen_tag)
    return original_request.urlencode()


@register.filter
def page_filter(request, chosen_page):
    chosen_page = str(chosen_page)
    original_request = request.GET.copy()
    original_request.setlist('page', chosen_page)
    return original_request.urlencode()


@register.filter
def get_favourite(recipe, user):
    return user.recipe_follower.filter(recipe=recipe).exists()


@register.filter
def get_purchase(recipe, user):
    return user.user_purchase.filter(recipe=recipe).exists()


@register.filter
def get_follow(author, user):
    return user.follower.filter(author=author).exists()


@register.filter
def get_author_id(username):
    user = get_object_or_404(User, username=username)
    return user.id


@register.filter
def get_suffix(value):
    value -= 3
    if value == 1 or (value > 20 and value % 10 == 1):
        return 'рецепт'
    elif 2 <= value <= 4 or (value > 20 and value % 10 in [2, 3, 4]):
        return 'рецепта'
    else:
        return 'рецептов'
