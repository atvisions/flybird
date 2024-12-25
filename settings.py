from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # 访问令牌有效期
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # 刷新令牌有效期
    'ROTATE_REFRESH_TOKENS': True,                   # 刷新令牌时是否生成新的刷新令牌
    'BLACKLIST_AFTER_ROTATION': True,                # 刷新后将旧的刷新令牌加入黑名单
    
    'AUTH_HEADER_TYPES': ('Bearer',),                # 认证头类型
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',        # 认证头名称
    
    'USER_ID_FIELD': 'id',                          # 用户ID字段
    'USER_ID_CLAIM': 'user_id',                     # 用户ID声明
} 