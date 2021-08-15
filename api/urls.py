from django.urls import path
from . import views

urlpatterns = [
    path('favorites/', views.add_favourite, name='add_favourite'),
    path('favorites/<int:id>/', views.remove_favourite, name='remove_favourite'),
    path('purchases/', views.add_purchase, name='add_purchase'),
    path('purchases/<int:id>/', views.remove_purchase, name='remove_purchase'),
    path('subscriptions/', views.subscribe, name='subscribe'),
    path('subscriptions/<int:id>/', views.unsubscribe, name='unsubscribe'),
    path('ingredients', views.IngredientList.as_view(), name='ingredients_list')
]
