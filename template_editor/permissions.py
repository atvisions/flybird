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