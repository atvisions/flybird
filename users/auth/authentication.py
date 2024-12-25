from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.utils.translation import gettext_lazy as _

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except InvalidToken:
            raise AuthenticationFailed(_('Token无效或已过期'))
        except Exception as e:
            raise AuthenticationFailed(_('认证失败'))

    def get_validated_token(self, raw_token):
        """重写此方法以自定义token验证逻辑"""
        try:
            return super().get_validated_token(raw_token)
        except Exception as e:
            raise InvalidToken(_('Token无效')) 