from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator

class IsNotDraftOrIsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.status == 'DRAFT' and obj.creator != request.user:
            raise PermissionDenied("Это объявление является черновиком и недоступно для просмотра.")
        return True
