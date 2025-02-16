from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#class User(models.Model) :

#    username = models.CharField(max_length=100, unique=True) #User's unique username
#    email = models.EmailField(unique=True) #User's unique email
#    created_at = models.DateTimeField(auto_now_add=True) #Timestamp when the user was created

#    def __str__(self):
#        return self.username
    
class Post (models.Model):

    POST_TYPES = {
        'text': 'Text Post',
        'image': 'Image Post',
        'video': 'Video Post'
    }

    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post_type = models.CharField(max_length=10, choices=POST_TYPES.items(), default='text')
    title = models.CharField(max_length=255, default='defaulttitle')  # Title field added
    content = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # content = models.TextField() # The text content of the post
    # #author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, default=1) # The user who created the post
    # created_at = models.DateTimeField(auto_now_add=True) # Timestamp when the post was created
    # is_published = models.BooleanField(default=False) # New Field to check if post has been published before

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"


class Comment(models.Model):
    text = models.TextField()
#    author = models.ForeignKey(User, related_name= 'comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}" 