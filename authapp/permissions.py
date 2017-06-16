from rest_framework.permissions import BasePermission
from rest_framework.permissions import is_authenticated


class IsUserTheUpdater(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj and is_authenticated(request.user)
