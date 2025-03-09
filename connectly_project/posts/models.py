from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    metadata = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, related_name= 'comments', on_delete=models.CASCADE, default=2)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}" 