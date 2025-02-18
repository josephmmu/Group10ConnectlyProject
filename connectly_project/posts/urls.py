from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views import PostViewSet
from .views import UserViewSet, CommentViewSet
from rest_framework.authtoken.views import obtain_auth_token
#from .views import UserViewSet,

router = DefaultRouter()
router.register(r'users', UserViewSet, basename = 'user')
router.register(r'posts', PostViewSet, basename = 'post')
router.register(r'comments', CommentViewSet, basename = 'comment')

urlpatterns = [
    # Include the the routers URL
    path('', include(router.urls)),

    # User registration URL
    #path ('register/', views.register, name = 'register'),

    # Self made user authentication
    #path('user-check/', views.authenticate_user, name = "user-authenticate"),

    # User registration URL
    #path ('get-user/', views.get_users, name = 'get-user-list'),

    # Token URL
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    #path('create/', CreatePostView.as_view(), name = 'create-post')

]
