from rest_framework import permissions

class IsTemplateCreator(permissions.BasePermission):
    """
    自定义权限类，用于检查用户是否是模板的创建者
    """
    def has_object_permission(self, request, view, obj):
        # 管理员可以编辑所有模板
        if request.user.is_staff:
            return True
        # 创建者可以编辑自己的模板
        return obj.creator == request.user 