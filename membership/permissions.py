from rest_framework import permissions
from django.utils import timezone

class IsMember(permissions.BasePermission):
    """检查是否是会员"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        membership = getattr(request.user, 'membership', None)
        if not membership or not membership.tier:
            return False
            
        if not membership.status:
            return False
            
        if membership.expire_time and membership.expire_time < timezone.now():
            return False
            
        return True

class HasMembershipPrivilege(permissions.BasePermission):
    """检查是否拥有会员权益"""
    def __init__(self, privilege_key):
        self.privilege_key = privilege_key
        
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        membership = getattr(request.user, 'membership', None)
        if not membership or not membership.tier:
            return False
            
        if not membership.status:
            return False
            
        if membership.expire_time and membership.expire_time < timezone.now():
            return False
            
        benefits = membership.tier.benefits
        if not benefits or self.privilege_key not in benefits:
            return False
            
        return True 