from django.http import request
from django.shortcuts import get_object_or_404
from recipes.models import Favourite, Ingredient, Purchase, Recipe, Follow
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import IngredientSerializer
from rest_framework import generics

User = get_user_model()


@api_view(["POST"])
def subscribe(request):
    author_id = request.data.get('id')
    to_follow = get_object_or_404(User, id=author_id)
    if (to_follow == request.user or
            Follow.objects.filter(user=request.user, author=to_follow).exists()):
        return Response({"success": "false"}, status=status.HTTP_400_BAD_REQUEST)
    Follow.objects.create(user=request.user, author=to_follow)
    return Response({"success": "true"}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def unsubscribe(request, id):
    main_user = request.user
    to_follow = get_object_or_404(User, id=id)
    following = Follow.objects.filter(user=main_user, author=to_follow)
    if following.exists():
        following.delete()
        return Response({"success": "true"})
    return Response({"success": "false"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def add_favourite(request):
    recipe_id = request.data.get('id')
    to_favourite = get_object_or_404(Recipe, id=recipe_id)
    if (to_favourite == request.user or
            Favourite.objects.filter(user=request.user, recipe=to_favourite).exists()):
        return Response({"success": "false"}, status=status.HTTP_400_BAD_REQUEST)
    Favourite.objects.create(user=request.user, recipe=to_favourite)
    return Response({"success": "true"}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def remove_favourite(request, id):
    main_user = request.user
    to_favourite = get_object_or_404(Recipe, id=id)
    favourite = Favourite.objects.filter(user=main_user, recipe=to_favourite)
    if favourite.exists():
        favourite.delete()
        return Response({"success": "true"})
    return Response({"success": "false"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def add_purchase(request):
    recipe_id = request.data.get('id')
    to_purchase = get_object_or_404(Recipe, id=recipe_id)
    if (to_purchase == request.user or
            Purchase.objects.filter(user=request.user, recipe=to_purchase).exists()):
        return Response({"success": "false"}, status=status.HTTP_400_BAD_REQUEST)
    Purchase.objects.create(user=request.user, recipe=to_purchase)
    return Response({"success": "true"}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def remove_purchase(request, id):
    main_user = request.user
    to_purchase = get_object_or_404(Recipe, id=id)
    following = Purchase.objects.filter(user=main_user, recipe=to_purchase)
    if following.exists():
        following.delete()
        return Response({"success": "true"})
    return Response({"success": "false"}, status=status.HTTP_400_BAD_REQUEST)


class IngredientList(generics.ListAPIView):
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('title',)

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        title = self.request.query_params.get('query')
        if title is not None:
            queryset = Ingredient.objects.filter(title__startswith=title)
        return queryset
