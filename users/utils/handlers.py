from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """自定义异常处理"""
    # 先调用REST framework默认的异常处理
    response = exception_handler(exc, context)
    
    if response is None:
        # 处理数据库异常
        if isinstance(exc, DatabaseError):
            response = Response({
                'detail': '数据库错误'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        # 处理Redis异常
        elif isinstance(exc, RedisError):
            response = Response({
                'detail': '缓存服务异常'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        # 处理其他未处理的异常
        else:
            response = Response({
                'detail': str(exc)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response 