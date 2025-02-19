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

    # Token URL
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
