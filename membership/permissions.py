from rest_framework import permissions
from django.utils import timezone

class IsPremiumUser(permissions.BasePermission):
    """检查是否是会员用户"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        membership = getattr(request.user, 'membership', None)
        if not membership or not membership.tier:
            return False
            
        if membership.tier.tier_type != 'premium':
            return False
            
        if membership.expire_time and membership.expire_time < timezone.now():
            return False
            
        return True

class HasPrivilege(permissions.BasePermission):
    """检查是否拥有特定权益"""
    def __init__(self, privilege_key):
        self.privilege_key = privilege_key
        
    def has_permission(self, request, view):
        from .services import MembershipService
        return MembershipService.check_privilege(request.user, self.privilege_key) 