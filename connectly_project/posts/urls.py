from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views import PostViewSet
from .views import UserViewSet, CommentViewSet
from rest_framework.authtoken.views import obtain_auth_token
from .views import login_view, logout_view, like_post, post_detail

from .views import post_list, edit_posts, delete_post

router = DefaultRouter()
router.register(r'users', UserViewSet, basename = 'user')
router.register(r'posts', PostViewSet, basename = 'post')
router.register(r'comments', CommentViewSet, basename = 'comment')

urlpatterns = [
    # Include the the routers URL
    path('api/', include(router.urls)),

    # Token URL
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('posts/', post_list, name="post-list"),

    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),

    path('post/<int:post_id>/', post_detail, name="post_detail"),
    path('post/<int:post_id>/like/', like_post, name="like_post"),

    path("post/<int:post_id>/edit/", edit_posts, name="edit_post"),
    path("post/<int:post_id>/delete/", delete_post, name="delete_post")


]
