from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
    
class IsOwnerOrBuyer(permissions.BasePermission):
    """
    allow a house owner or a purchase buyer access to the house unit
    """

    def has_object_permission(self, request, view, obj):
        is_owner = obj.house.owner == request.user
        is_buyer = obj.buyer == request.user
        
        return is_owner or is_buyer