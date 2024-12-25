from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework import status

def custom_exception_handler(exc, context):
    """自定义异常处理"""
    response = exception_handler(exc, context)
    
    if response is None:
        if isinstance(exc, ValidationError):
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'errors': exc.messages
            }, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
            'code': 500,
            'message': str(exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # 统一响应格式
    if not isinstance(response.data, dict):
        response.data = {
            'code': response.status_code,
            'message': response.data
        }
    elif 'detail' in response.data:
        response.data = {
            'code': response.status_code,
            'message': response.data['detail']
        }
    else:
        response.data = {
            'code': response.status_code,
            'message': '请求失败',
            'errors': response.data
        }
    
    return response 