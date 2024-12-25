from django.urls import get_resolver
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def list_urls(request):
    """
    列出所有可用的API端点
    """
    url_patterns = []
    resolver = get_resolver()
    
    def collect_urls(patterns, prefix=''):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                collect_urls(pattern.url_patterns, prefix + str(pattern.pattern))
            else:
                full_path = prefix + str(pattern.pattern)
                if 'admin' not in full_path:
                    url_patterns.append({
                        'path': full_path,
                        'name': pattern.name if pattern.name else 'unnamed',
                        'method': pattern.callback.__name__ if hasattr(pattern, 'callback') else 'unknown'
                    })
    
    collect_urls(resolver.url_patterns)
    return Response(url_patterns)