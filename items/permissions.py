from rest_framework import permissions


class IsPermitted(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.method == 'PUT' or request.method == "PATCH" or request.method == "DELETE":
            return obj.owner == request.user
        if request.method == 'POST':
            return request.user.is_authenticated()
