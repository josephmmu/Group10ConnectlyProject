from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Post, Comment   
#from .models import User
from .serializers import PostSerializer, CommentSerializer
#from .serializers import UserSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.views import APIView
# import Response
# import status
from .factories.post_factory import PostFactory


# Create your views here.

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.create_user(username = username, password = password)

        return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
    

@api_view(['GET'])
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all().values('id', 'username')
    return Response({"users": list(users)}, status=status.HTTP_200_OK)


class CreatePostView(APIView):
    def post(self, request):
        data = request.data

        try :
            post = PostFactory.create_post(
                post_type = data ['post_type'],
                title = data ['title'],
                content = data.get('content', ''),
                metadata = data.get('metadata', {})
            )
            return Response({'message': 'Post created successfully!', 'post_id': post.id}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PostViewSet(viewsets.ModelViewSet):
     queryset = Post.objects.all()
     serializer_class = PostSerializer
     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data = request.data)
#         serializer.is_valid(raise_exception = True)
#         self.perform_create(serializer)
#         return Response({"message": " Post created successfully", "data": serializer.data}, status = status.HTTP_201_CREATED)
    
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data = request.data, partial = partial)
#         serializer.is_valid(raise_exception = True)
#         self.perform_update(serializer)
#         return Response({"message": " Post Updated successfully", "data": serializer.data}, status = status.HTTP_200_OK)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if instance.completed:
#             return Response({"error": "Cannot delete the Post"}, status = status.HTTP_400_BAD_REQUEST)
#         self.perform_destroy(instance)
#         return Response({"message": " Post deleted successfully"}, status = status.HTTP_204_NO_CONTENT)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        return Response({"message": " Comment created successfully", "data": serializer.data}, status = status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data, partial = partial)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)
        return Response({"message": " Comment Updated successfully", "data": serializer.data}, status = status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.completed:
            return Response({"error": "Cannot delete the Comment"}, status = status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response({"message": " Comment deleted successfully"}, status = status.HTTP_204_NO_CONTENT)
    
