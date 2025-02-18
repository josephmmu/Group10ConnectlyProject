from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Post, Comment   
#from .models import User
from .serializers import UserSerializer, PostSerializer, CommentSerializer
#from .serializers import UserSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.views import APIView
# import Response
# import status
from .factories.post_factory import PostFactory

from django.contrib.auth import authenticate

from .permissions import IsAuthorOrAdmin, IsAdminUser


# Create your views here.

#Viewset for User Managment
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

# @api_view(['POST'])
# def register(request):
#     if request.method == 'POST':
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = User.objects.create_user(username = username, password = password)

#         return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
    
# method for access control to authenticate users
# @api_view(['POST'])
# def authenticate_user(request):
#     if request.method == 'POST':
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username = username, password = password)

#         if user is not None:
#             return Response({"message": "User is validated in the database"}, status= status.HTTP_302_FOUND)
#         else:
#             return Response({"message": "User is not found in the database :("}, status = status.HTTP_404_NOT_FOUND)

# @api_view(['GET'])
# def get_users(request):
#     if request.method == 'GET':
#         users = User.objects.all().values('id', 'username')
#     return Response({"users": list(users)}, status=status.HTTP_200_OK)


# class CreatePostView(APIView):
#     def post(self, request):
#         data = request.data

#         try :
#             post = PostFactory.create_post(
#                 post_type = data ['post_type'],
#                 title = data ['title'],
#                 content = data.get('content', ''),
#                 metadata = data.get('metadata', {})
#             )
#             return Response({'message': 'Post created successfully!', 'post_id': post.id}, status=status.HTTP_201_CREATED)
#         except ValueError as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# Hopefully the last view I need to edit
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthorOrAdmin]

    def create(self, request, *args, **kwargs):
        # Override update to add custom error handling
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # Ensure author is set
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        # Override update to add custom error handling
        instance = self.get_object()
        if not IsAuthorOrAdmin().has_object_permission(request, self, instance):
            return Response({"error": "You are not allowed to edit this post."}, status = status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        
        instance = self.get_object()
        if not IsAuthorOrAdmin().has_object_permission(request, self, instance):
            return Response({"error": "You are not allowed to delete this post."}, status = status.HTTP_403_FORBIDDEN)
        
        print(f"Post '{instance.title} (ID: {instance.id}) deleted by {request.user}")
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthorOrAdmin]

    def create(self, request, *args, **kwargs):
        # Ensure the author is set from the authenticated user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Force the author to be the authenticated user
        serializer.save(author=request.user)

        return Response({"message": "Comment created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not IsAuthorOrAdmin().has_object_permission(request, self, instance):
            return Response({"error": "You are not allowed to update this comment."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Comment updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not IsAuthorOrAdmin().has_object_permission(request, self, instance):
            return Response({"error": "You are not allowed to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
