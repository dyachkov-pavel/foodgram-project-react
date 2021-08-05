from recipes.forms import RecipeForm
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from .models import Favourite, Ingredient, Purchase, Recipe, RecipeIngredient, Tag, Follow
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .add_ingredients import add_ingredients


User = get_user_model()


def index(request):
    tag_list = request.GET.getlist('tags', -1)
    if tag_list == -1:
        recipe_list = Recipe.objects.all()
    else:
        recipe_list = Recipe.objects.filter(tag__slug__in=tag_list).distinct()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'indexAuth.html',
        {'page': page,
         'paginator': paginator,
         'all_tags': Tag.objects.all(),
         'tag_list': tag_list}
    )


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)
    used_ingredients = recipe.recipes.all()
    return render(
        request,
        'singlePage.html',
        {'recipe': recipe,
         'used_ingredients': used_ingredients}
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
    author = get_object_or_404(User, username=username)
    tag_list = request.GET.getlist('tags', -1)
    if tag_list == -1:
        recipe_list = author.user_recipes.all()
    else:
        recipe_list = author.user_recipes.filter(
            tag__slug__in=tag_list).distinct()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'authorRecipe.html',
        {'author': author,
         'page': page,
         'paginator': paginator,
         'all_tags': Tag.objects.all(),
         'tag_list': tag_list}
    )


@login_required
def create_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        print(form.instance.tag.all())
        add_ingredients(request, form.instance)
        return redirect("index")
    return render(request, "formRecipe.html", {"form": form})


@login_required
def edit_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe', usermame=username, recipe_id=recipe_id)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)
    used_ingredients = recipe.recipes.all()
    if form.is_valid():
        form.save()
        add_ingredients(request, recipe)
        return redirect('recipe', username=username, recipe_id=recipe_id)
    return render(request,
                  'formRecipe.html',
                  {
                    'recipe': recipe,
                    'used_ingredients': used_ingredients,
                    'update': True,
                    'form': form
                  }
                  )


@login_required
def delete_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe', username=username, recipe_id=recipe_id)
    recipe.delete()
    return redirect('index')


def favourite(request):
    tag_list = request.GET.getlist('tags', -1)
    if tag_list == -1:
        favourite_list = request.user.recipe_follower.all()
    else:
        favourite_list = request.user.recipe_follower.filter(
            recipe__tag__slug__in=tag_list).distinct()
    paginator = Paginator(favourite_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'favorite.html',
        {
            'page': page,
            'paginator': paginator,
            'all_tags': Tag.objects.all(),
            'tag_list': tag_list
        }
    )


def purchases(request):
    purchases = request.user.user_purchase.all()
    return render(request, 'shopList.html', {'purchases': purchases})


def purchase_delete(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    purchase = recipe.recipe_purchase.filter(recipe=recipe, user=request.user)
    if purchase.exists():
        purchase.delete()
    return redirect('purchases')


def download_txt(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'
    purchases = request.user.user_purchase.all()
    lines = ['Продуктовый помощник\n\n']
    shoplist = {}
    for purchase in purchases:
        recipe = purchase.recipe
        used_ingredients = recipe.recipes.all()
        for used_ingredient in used_ingredients:
            ingredient_name = used_ingredient.ingredient.title
            ingredient_quantity = used_ingredient.quantity
            ingredient_dimension = used_ingredient.ingredient.dimension
            if ingredient_name not in shoplist:
                shoplist[ingredient_name] = [
                    ingredient_quantity, ingredient_dimension]
            else:
                shoplist[ingredient_name][0] += ingredient_quantity
    for key, value in shoplist.items():
        lines.append(f'{key}: {value[0]} {value[1]}\n')
    response.writelines(lines)
    return response


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
