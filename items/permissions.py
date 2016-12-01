from rest_framework import permissions

SAFE_METHODS = ["GET", "HEAD", "OPTION"]


class ReadOnlyIfNotConnected(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_authenticated()
