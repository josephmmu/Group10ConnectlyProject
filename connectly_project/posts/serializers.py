from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
            } # Ensures password is not returned

        def create(self, validated_data):
            request = self.context.get('request')

            # Ensure request exists (prevents anonymous requests from setting staff/superuser)
            if not request or not request.user or not request.user.is_authenticated:
                validated_data.pop('is_staff', None)
                validated_data.pop('is_superuser', None)

            # If the user is NOT a superuser, force 'is_staff' and 'is_superuser' to False
            if not request.user.is_superuser:
                validated_data.pop('is_staff', None)
                validated_data.pop('is_superuser', None)
                

            user = User.objects.create_user(**validated_data)
            return user

class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')    

    
    class Meta:
        model = Post
        fields = ['id', 'author', 'post_type', 'title', 'content', 'metadata']
        read_only_fields = ['author', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at']
        read_only_fields = ['author', 'created_at']
        
    def validate_post(self, value):
        if not Post.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Post not found.")
        return value
    
    def validate_author(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError('Author not found.')
        return value