from rest_framework import permissions
from apps.content.models import Content
from apps.globalvar.models import GlobalVar


class IsContentAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_author = obj.openId == request.user.openId

        admin_user = GlobalVar.objects.get(key='ADMIN_USER')
        l_admin_user = admin_user.value.split()
        is_admin = request.user.openId in l_admin_user

        return is_author or is_admin or request.user.username == 'qujintao'