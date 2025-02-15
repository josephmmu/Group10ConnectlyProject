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



# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         serializer = self.get_serializer(instance, data = request.data, partial = partial)
#         serializer.is_valid(raise_exception = True)
#         self.perform_update(serializer)
#         return Response({"message": " User Updated successfully", "data": serializer.data}, status = status.HTTP_200_OK)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if instance.completed:
#             return Response({"error": "Cannot delete the user"}, status = status.HTTP_400_BAD_REQUEST)
#         self.perform_destroy(instance)
#         return Response({"message": " User deleted successfully"}, status = status.HTTP_204_NO_CONTENT)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        return Response({"message": " Post created successfully", "data": serializer.data}, status = status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data, partial = partial)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)
        return Response({"message": " Post Updated successfully", "data": serializer.data}, status = status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.completed:
            return Response({"error": "Cannot delete the Post"}, status = status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response({"message": " Post deleted successfully"}, status = status.HTTP_204_NO_CONTENT)

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
    
#class UserListCreate(APIView):
#
#    def get(self, request):
#        users = User.objects.all()
#        serializer = UserSerializer(users, many=True)
#        return Response(serializer.data)
#    
#    def post(self, request):
#        serializer = UserSerializer(data = request.data)
#        if serializer.is_valid():
#            serializer.save() 
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#class PostListCreate(APIView):
#    def get(self, request):
#        posts = Post.objects.all()
#        serializer = PostSerializer(posts, many=True)
#        return Response(serializer.data)
#    
#    def post(self, request):
#        serializer = PostSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#class CommentListCreate(APIView):
#    def get(self, request):
#        comments = Comment.objects.all()
#        serializer = CommentSerializer(comments, many=True)
#        return Response(serializer.data)
    
#    def post(self, request):
#        serializer = CommentSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)