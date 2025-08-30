from rest_framework import permissions


class IsLandlordOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.profile.is_landlord
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.landlord == request.user
    
class IsTenantOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow tenants to do  their own applications.
    Read permissions are allowed to all.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and not request.user.profile.is_landlord

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.tenant == request.user

class IsLandlordOrTenant(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow only authenticated users can access this.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # allow landlords to access their own house's applications/agreements.
        if request.user.profile.is_landlord:
            return obj.application.house.landlord == request.user
        # allo tenats to access their applications
        return obj.application.tenant == request.user