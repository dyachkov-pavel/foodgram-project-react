from django.http import request
from django.shortcuts import get_object_or_404
from recipes.models import Favourite, Ingredient, Purchase, Recipe, Follow
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import IngredientSerializer
from rest_framework import generics

User = get_user_model()

HTTP_200_RESPONSE = Response({'success': 'true'})
HTTP_201_RESPONSE = Response({'success': 'true'}, HTTP_201_CREATED)
HTTP_400_RESPONSE = Response({'success': 'false'}, HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def subscribe(request):
    author_id = request.data.get('id')
    to_follow = get_object_or_404(User, id=author_id)
    user = request.user
    if (to_follow == request.user or
            Follow.objects.filter(user=user,
                                  author=to_follow).exists()):
        return HTTP_400_RESPONSE
    Follow.objects.create(user=request.user, author=to_follow)
    return HTTP_201_RESPONSE


@api_view(['DELETE'])
def unsubscribe(request, id):
    main_user = request.user
    to_follow = get_object_or_404(User, id=id)
    following = Follow.objects.filter(user=main_user,
                                      author=to_follow)
    if following.exists():
        following.delete()
        return HTTP_200_RESPONSE
    return HTTP_400_RESPONSE


@api_view(['POST'])
def add_favourite(request):
    recipe_id = request.data.get('id')
    to_favourite = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    if (to_favourite == request.user or
            Favourite.objects.filter(user=user,
                                     recipe=to_favourite).exists()):
        return HTTP_400_RESPONSE
    Favourite.objects.create(user=user, recipe=to_favourite)
    return HTTP_201_RESPONSE


@api_view(['DELETE'])
def remove_favourite(request, id):
    main_user = request.user
    to_favourite = get_object_or_404(Recipe, id=id)
    favourite = Favourite.objects.filter(user=main_user,
                                         recipe=to_favourite)
    if favourite.exists():
        favourite.delete()
        return HTTP_200_RESPONSE
    return HTTP_400_RESPONSE


@api_view(['POST'])
def add_purchase(request):
    recipe_id = request.data.get('id')
    to_purchase = get_object_or_404(Recipe, id=recipe_id)
    if (to_purchase == request.user or
            Purchase.objects.filter(user=request.user,
                                    recipe=to_purchase).exists()):
        return HTTP_400_RESPONSE
    Purchase.objects.create(user=request.user, recipe=to_purchase)
    return HTTP_201_RESPONSE


@api_view(['DELETE'])
def remove_purchase(request, id):
    main_user = request.user
    to_purchase = get_object_or_404(Recipe, id=id)
    following = Purchase.objects.filter(user=main_user, recipe=to_purchase)
    if following.exists():
        following.delete()
        return HTTP_200_RESPONSE
    return HTTP_400_RESPONSE


class IngredientList(generics.ListAPIView):
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('title',)

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        title = self.request.query_params.get('query').lower()
        if title is not None:
            queryset = Ingredient.objects.filter(title__startswith=title)
        return queryset
