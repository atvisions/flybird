# template_editor/permissions.py
from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    只允许管理员创建、修改和删除，其他用户只能查看
    """
    def has_permission(self, request, view):
        # 允许所有用户进行只读操作（GET, HEAD, OPTIONS）
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 写操作只允许管理员
        return request.user and request.user.is_staff

class CanModifyTemplate(permissions.BasePermission):
    """
    检查用户是否有权限修改模板：
    1. 管理员可以修改任何模板
    2. 创建者可以修改自己的模板(修改已发布的模板会重新进入审核状态)
    """
    def has_object_permission(self, request, view, obj):
        # 允许所有用户进行只读操作
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # 管理员可以修改任何模板
        if request.user.is_staff:
            return True
            
        # 非管理员只能修改自己创建的模板
        if obj.creator != request.user:
            return False
            
        # 允许创建者修改任何状态的模板
        return True