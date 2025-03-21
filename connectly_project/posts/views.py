from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from .models import Post, Comment   
from .serializers import UserSerializer, PostSerializer, CommentSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import TokenAuthentication

from rest_framework.views import APIView
from .factories.post_factory import PostFactory

from .permissions import IsAuthorOrAdmin

from .singletons.logger_singleton import LoggerSingleton

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from django.core.exceptions import PermissionDenied
from posts.forms import PostForm

from django.db.models import Q

# function to run gui site

@login_required
def liked_posts(request):
    user = request.user  # Get the currently logged-in user
    liked_posts = Post.objects.filter(likes=user)  # Filter posts the user liked
    return render(request, "liked_posts.html", {"posts": liked_posts})

@login_required
def toggle_privacy(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.is_private = not post.is_private
    post.save()
    return redirect("post-list")


# List of Posts Page
@login_required
def post_list(request):

    user = request.user

    # For showing liked posts
    show_liked = request.GET.get("liked") == "true"  # Check if the user wants to filter liked posts
    if show_liked:
        posts = Post.objects.filter(likes=user)  # Show only liked posts
    else:
        posts = Post.objects.all()  # Show all posts


    # For private/public posts and only allowing admins view access
    if user.is_staff:  # Admins/Staff can see all posts
        posts = Post.objects.all()
    else:  # Regular users only see public posts or their own private posts
        posts = Post.objects.filter(Q(is_private=False) | Q(author=user))

    # Sort logic
    user_id = request.GET.get('user')
    sort_by = request.GET.get('sort', '-created_at')

    posts = Post.objects.all().order_by(sort_by) #to order posts
    users = User.objects.all()

    if user_id:
        posts = posts.filter(author_id = user_id)

    paginator = Paginator(posts, 5) # Going to be showing 5 posts per page

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'index.html', {'posts': posts, 'users': users, 'show_liked': show_liked})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "post_detail.html", {"post": post})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user) # Removes the like if its already liked
    else: 
        post.likes.add(request.user) # Likes if its not liked yet
        
    return redirect("post_detail", post_id=post.id) #Redirect back to pst detail

# Create your views here.

#Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("post-list")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

#Logout View
def logout_view(request):
    logout(request)
    return redirect("login")

# Edit Posts View
@login_required
def edit_posts(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    #Only allowing the author, staff, or superusers
    if request.user != post.author and not request.user.is_staff:
        raise PermissionDenied
    
    if request.method == "POST":
        form = PostForm(request.POST, instance = post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id = post_id)
    else:
        form = PostForm(instance = post)

    return render(request, "edit_post.html", {"form": form, "post": post})  


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)

    #Only allowing the author, staff, or superusers
    if request.user != post.author and not request.user.is_staff:
        raise PermissionDenied
    
    if request.method == "POST":
        post.delete()
        return redirect("post-list")
    
    return render(request, "delete_post.html", {"post": post})

#Viewset for User Managment
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthorOrAdmin]
    
    def get_permissions(self):
        """ Allows anyone to create a user, but require admin for updates."""
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAdminUser()]

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