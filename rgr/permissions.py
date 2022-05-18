from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_staff):
            return True
        else:
            return view.action in ['retrieve','update','partial_update','destroy']

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or bool(request.user and request.user.is_staff)


