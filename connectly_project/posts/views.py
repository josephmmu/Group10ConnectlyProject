from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Post, Comment   
from .serializers import UserSerializer, PostSerializer, CommentSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.views import APIView
from .factories.post_factory import PostFactory

from .permissions import IsAuthorOrAdmin

from .singletons.logger_singleton import LoggerSingleton

# Create your views here.

#Viewset for User Managment
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthorOrAdmin]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthorOrAdmin]

    def create(self, request, *args, **kwargs):
        logger = LoggerSingleton().get_logger()
        logger.info("Received a request to create a new post.")

        data = request.data
        title = data.get("title")
        content = data.get("content", "")
        post_type = data.get("post_type")
        metadata = data.get("metadata", {})

        try:
            post = PostFactory.create_post(post_type, title, content, metadata)
            post.author = request.user
            post.save()

            serializer = self.get_serializer(post)
            logger.info("New Post Created successfully.")
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        except ValueError as e:
            logger.error(f"Failed to create a new post: {str(e)}")
            return Response({"error": str(e)}, status = status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        logger = LoggerSingleton().get_logger()
        logger.info("Received a request to udpate a post.")
        # Override update to add custom error handling
        instance = self.get_object()
        if not IsAuthorOrAdmin().has_object_permission(request, self, instance):
            logger.info("Post updated successfully.")
            return Response({"error": "You are not allowed to edit this post."}, status = status.HTTP_403_FORBIDDEN)
        else:
            logger.error("Failed to update post. Errors: %s", serializer.errors)
            return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        logger = LoggerSingleton().get_logger()
        logger.info("Received a request to delete a post.")
        
        instance = self.get_object()
        if not IsAuthorOrAdmin().has_object_permission(request, self, instance):
            logger.error("Failed to delete post. Errors: %s", serializer.errors)
            return Response({"error": "You are not allowed to delete this post."}, status = status.HTTP_403_FORBIDDEN)
        else:
            logger.info("Post deleted successfully.")
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
        logger = LoggerSingleton().get_logger()
        logger.info("Received a request to udpate a post.")

        instance = self.get_object()
        if not IsAuthorOrAdmin().has_object_permission(request, self, instance):
            logger.error("Failed to update post. Errors: %s", serializer.errors)
            return Response({"error": "You are not allowed to update this comment."}, status=status.HTTP_403_FORBIDDEN)
        else:   
            serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop('partial', False))
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            logger.info("Post updated successfully.")
            return Response({"message": "Comment updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        logger = LoggerSingleton().get_logger()
        logger.info("Received a request to delete a post.")
        instance = self.get_object()
        if not IsAuthorOrAdmin().has_object_permission(request, self, instance):
            logger.error("Failed to delete post. Errors: %s", serializer.errors)
            return Response({"error": "You are not allowed to delete this comment."}, status=status.HTTP_403_FORBIDDEN)
        else:
            logger.info("Post deleted successfully.")
            self.perform_destroy(instance)
            return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)