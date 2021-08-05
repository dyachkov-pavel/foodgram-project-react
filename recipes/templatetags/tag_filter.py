from django import template
from django.contrib.auth import get_user_model
from django.http import request


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
def substract(value, arg=3):
    return value - arg


@register.filter
def three_recipes(value):
    return value[:3]


@register.filter
def get_favourite(recipe, user):
    return user.recipe_follower.filter(recipe=recipe).exists()


@register.filter
def purchase_counter(user):
    return user.user_purchase.count()


@register.filter
def get_purchase(recipe, user):
    return user.user_purchase.filter(recipe=recipe).exists()


@register.filter
def get_follow(author, user):
    return user.follower.filter(author=author).exists()

@register.filter
def get_author_id(username):
    user = User.objects.get(username=username)
    return user.id
