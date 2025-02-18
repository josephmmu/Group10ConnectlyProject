import logging
from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)

class IsPostAuthor(BasePermission):
    # Allows access only to the author of the post
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
class IsAuthorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated


    # Allows access only to the author of the post
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            logger.info(f"Admin {request.user} is modifying Post ID {obj.id}")
            return True
        logger.warning(f"User {request.user} attempted to modify Post ID {obj.id}")
        return obj.author == request.user

class IsAdminUser(BasePermission):
    # Allows access only to admin users
    def has_permission(self, request, view):
        return request.user and request.user.is_staff