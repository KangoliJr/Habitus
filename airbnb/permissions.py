from rest_framework import permissions

"""
    Creating a custom permission that only allows  owners of the house to edit it.
    Read-only access is allowed for anyone 
"""
class IsHostOrReadOnly(permissions.BasePermission):
 
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_host
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.host == request.user