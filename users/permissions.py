from rest_framework import permissions


class IsUserHimself(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsUserOfProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
