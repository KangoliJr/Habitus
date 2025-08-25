from rest_framework import permissions

"""
    Creating a custom permission that only allows  owners of the house to edit it.
    Read-only access is allowed for anyone 
"""
class IsHostOrReadOnly(permissions.BasePermission):
 
    def has_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.host == request.user
    
  