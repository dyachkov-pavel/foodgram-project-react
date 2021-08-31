from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-recipe/', views.create_recipe, name='new_recipe'),
    path('download_txt/', views.download_txt, name='download_txt'),
    path('favourite/', views.favourite, name='favourite'),
    path('follow/', views.follow_index, name='follow'),
    path('purchases/', views.purchases, name='purchases'),
    path('purchases/<int:id>/delete/',
         views.purchase_delete,
         name='purchase_delete'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:recipe_id>/',
         views.recipe_view,
         name='recipe'),
    path('<str:username>/<int:recipe_id>/delete/',
         views.delete_recipe,
         name='delete_recipe'),
    path('<str:username>/<int:recipe_id>/edit/',
         views.edit_recipe,
         name='edit_recipe'),
]
