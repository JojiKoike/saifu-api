from rest_framework import permissions


class IsOwnerOnlyFullAccess(permissions.BasePermission):
    """
    Object-Level permission to only allow owners full access
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
