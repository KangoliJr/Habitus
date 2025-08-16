from rest_framework import permissions

class IsHost(permissions.BasePermission):
    """
    Custom permission to only allow hosts to create, update, or delete an object.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_host
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True 
        
        return obj.host == request.user