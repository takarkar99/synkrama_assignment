from rest_framework import permissions


class IsSuperOrOwner(permissions.BasePermission):



    def has_object_permission(self, request, view, obj):

        if request.user and request.user.is_superuser:
            return True
        
        return obj.author == request.user