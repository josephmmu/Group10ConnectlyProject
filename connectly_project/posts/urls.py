from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.get_users, name='get_user'),
    path('users/create/', views.create_user, name='create_user'),
    path('posts/', views.get_post, name='get_posts'),
    path('posts/create/', views.create_post, name='create_post'),
]