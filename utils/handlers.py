from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # 先调用 REST framework 默认的异常处理
    response = exception_handler(exc, context)

    if response is None:
        # 如果 DRF 没有处理这个异常，我们自己处理
        return Response({
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': str(exc),
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 自定义响应格式
    return Response({
        'code': response.status_code,
        'message': str(exc),
        'data': response.data if hasattr(response, 'data') else None
    }, status=response.status_code) 