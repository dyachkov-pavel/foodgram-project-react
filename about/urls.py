from django.urls import path
from . import views


urlpatterns = [
    path('author/', views.AboutAuthor.as_view(), name='author'),
    path('foodgram/', views.AboutFoodgram.as_view(), name='foodgram'),
    path('tech/', views.AboutTech.as_view(), name='tech'),
] 
