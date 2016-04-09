from rest_framework import permissions
# from permissions.manage import has_all_permissions
# 
# 
# # from glims.jobs import JobFactory
# # from models import 
# class CustomPermission(permissions.BasePermission):
#     """
#     Object-level permission to only allow owners of an object to edit it.
#     Assumes the model instance has an `owner` attribute.
#     """
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:            
#             return True
# 
#         # Instance must have an attribute named `owner`.
#         return has_all_permissions(request.user, obj, ['admin'])
class GroupPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        group = obj.get_group()
        if not group:
            return False
        return request.user.groups.filter(id=group.id).exists()

class AdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
