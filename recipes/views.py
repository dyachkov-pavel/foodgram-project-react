from django.db.models.aggregates import Sum
from recipes.forms import RecipeForm
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, RecipeIngredient, Tag
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.http import HttpResponse


User = get_user_model()


def index(request):
    tags = {}
    tag_list = request.GET.getlist('tags')
    if not tag_list:
        recipes = Recipe.objects.all()
    else:
        recipes = Recipe.objects.filter(tag__slug__in=tag_list).distinct()
    for tag in Tag.objects.all():
        if tag.slug in tag_list:
            tags[tag.slug] = [True, tag]
        else:
            tags[tag.slug] = [False, tag]
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'indexAuth.html',
        {'page': page,
         'paginator': paginator,
         'tags': tags, }
    )


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe,
                               id=recipe_id,
                               author__username=username)
    return render(
        request,
        'singlePage.html',
        {'recipe': recipe, }
    )


@login_required
def follow_index(request):
    followed_authors = request.user.follower.all()
    paginator = Paginator(followed_authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'myFollow.html',
        {'page': page,
         'paginator': paginator,
         'followed_authors': followed_authors}
    )


def profile(request, username):
    tags = {}
    author = get_object_or_404(User, username=username)
    tag_list = request.GET.getlist('tags')
    if not tag_list:
        recipe_list = author.user_recipes.all()
    else:
        recipe_list = author.user_recipes.filter(
            tag__slug__in=tag_list).distinct()
    for tag in Tag.objects.all():
        if tag.slug in tag_list:
            tags[tag.slug] = [True, tag]
        else:
            tags[tag.slug] = [False, tag]
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'authorRecipe.html',
        {'author': author,
         'page': page,
         'paginator': paginator,
         'tags': tags, }
    )


@login_required
def create_recipe(request):
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      request=request)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('index')
    return render(request, 'formRecipe.html', {'form': form})


@login_required
def edit_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe,
                               author__username=username,
                               id=recipe_id)
    if request.user != recipe.author and not request.user.is_staff:
        return redirect('recipe', usermame=username, recipe_id=recipe_id)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe,
                      request=request)
    if form.is_valid():
        form.save()
        return redirect('recipe', username=username, recipe_id=recipe_id)
    return render(request,
                  'formRecipe.html',
                  {'recipe': recipe,
                   'update': True,
                   'form': form}
                  )


@login_required
def delete_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe,
                               author__username=username,
                               id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe', username=username, recipe_id=recipe_id)
    recipe.delete()
    return redirect('index')


def favourite(request):
    tags = {}
    tag_list = request.GET.getlist('tags')
    if not tag_list:
        favourite_list = request.user.recipe_follower.all()
    else:
        favourite_list = request.user.recipe_follower.filter(
            recipe__tag__slug__in=tag_list).distinct()
    for tag in Tag.objects.all():
        if tag.slug in tag_list:
            tags[tag.slug] = [True, tag]
        else:
            tags[tag.slug] = [False, tag]
    paginator = Paginator(favourite_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'favorite.html',
        {'page': page,
         'paginator': paginator,
         'tags': tags, }
    )


def purchases(request):
    purchases = request.user.user_purchase.all()
    return render(request, 'shopList.html', {'purchases': purchases})


def purchase_delete(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    purchase = recipe.recipe_purchase.filter(recipe=recipe,
                                             user=request.user)
    if purchase.exists():
        purchase.delete()
    return redirect('purchases')


def download_txt(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'
    lines = ['Продуктовый помощник\n\n']
    purchases = RecipeIngredient.objects.filter(
        recipe__in=request.user.user_purchase.values('recipe')).values(
        'ingredient__title', 'ingredient__dimension').annotate(
        quantity=Sum('quantity')
    )
    for purchase in purchases:
        ingredient_name = purchase['ingredient__title']
        ingredient_quantity = purchase['quantity']
        ingredient_dimension = purchase['ingredient__dimension']
        lines.append(
            f'{ingredient_name}: {ingredient_quantity} '
            f'{ingredient_dimension}\n'
        )
    response.writelines(lines)
    return response


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
