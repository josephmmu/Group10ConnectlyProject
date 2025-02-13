from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views import PostViewSet, CommentViewSet
#from .views import UserViewSet,

#urlpatterns = [
#    path('users/', UserListCreate.as_view(), name='user-list-create'),
#    path('posts/', PostListCreate.as_view(), name='post-list-create'),
#    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
#]

router = DefaultRouter()
#router.register(r'users', UserViewSet, basename = 'user')
router.register(r'posts', PostViewSet, basename = 'post')
router.register(r'comments', CommentViewSet, basename = 'comment')

urlpatterns = [
    # Include the the routers URL
    path('', include(router.urls)),

    # User registration URL
    path ('register/', views.register, name = 'register')

]