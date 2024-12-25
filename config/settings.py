import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ----------- 1. 核心配置 -----------
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ----------- 2. 域名配置 -----------
BASE_DOMAIN = os.getenv('BASE_DOMAIN', 'popo.work')
BACKEND_DOMAIN = os.getenv('BACKEND_DOMAIN', 'www.popo.work:8000')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://popo.work')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.186.162',
    '0.0.0.0',
    '*',  # 开发环境可以允许所有主机
]

# ----------- 3. 应用配置 -----------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_filters',
]

LOCAL_APPS = [
    'users.apps.UsersConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ----------- 4. 中间件配置 -----------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ----------- 5. 模板配置 -----------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ----------- 6. 数据库配置 -----------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'connect_timeout': 60,
        },
        'CONN_MAX_AGE': 60,  # 数据库连接的最大生命周期（秒）
    }
}

# ----------- 7. 缓存配置 -----------
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_DB = os.getenv('REDIS_DB', '1')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PASSWORD": REDIS_PASSWORD if REDIS_PASSWORD else None,
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "RETRY_ON_TIMEOUT": True,
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        },
        "KEY_PREFIX": "popo",
    }
}

# Session 配置
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# ----------- 8. 认证配置 -----------
AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# JWT配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# ----------- 9. REST Framework配置 -----------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ) if not DEBUG else (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': int(os.getenv('PAGE_SIZE', '10')),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    },
    'EXCEPTION_HANDLER': 'utils.handlers.custom_exception_handler',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}

# ----------- 10. CORS配置 -----------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://192.168.186.162:8080",
    "http://0.0.0.0:8080",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ----------- 11. 文件上传配置 -----------
FILE_UPLOAD_SETTINGS = {
    'ALLOWED_TYPES': {
        'image': ['image/jpeg', 'image/png', 'image/gif'],
        'document': ['application/pdf', 'application/msword'],
        'video': ['video/mp4'],
    },
    'MAX_SIZE': {
        'image': 5 * 1024 * 1024,  # 5MB
        'document': 10 * 1024 * 1024,  # 10MB
        'video': 50 * 1024 * 1024,  # 50MB
    }
}

# ----------- 12. 日志配置 -----------
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'django.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'error.log',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'users': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        }
    }
}

# ----------- 13. 静态文件配置 -----------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ----------- 14. 国际化配置 -----------
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# ----------- 15. 第三方服务配置 -----------
# 阿里云配置
ALIYUN = {
    'ACCESS_KEY_ID': os.getenv('ALIYUN_ACCESS_KEY_ID'),
    'ACCESS_KEY_SECRET': os.getenv('ALIYUN_ACCESS_KEY_SECRET'),
    'SMS_SIGN_NAME': os.getenv('ALIYUN_SMS_SIGN_NAME'),
    'SMS_TEMPLATES': {
        'register': os.getenv('SMS_TPL_REGISTER', 'SMS_476545109'),
        'login': os.getenv('SMS_TPL_LOGIN', 'SMS_476520108'),
        'reset_password': os.getenv('SMS_TPL_RESET_PWD', 'SMS_476275121'),
        'change_phone': os.getenv('SMS_TPL_CHANGE_PHONE', 'SMS_476500294'),
    }
}

# 微信配置
WECHAT = {
    'APP_ID': os.getenv('WECHAT_APP_ID'),
    'APP_SECRET': os.getenv('WECHAT_APP_SECRET'),
    'MP_APP_ID': os.getenv('WECHAT_MP_APP_ID'),
    'MP_APP_SECRET': os.getenv('WECHAT_MP_APP_SECRET'),
    'MP_TOKEN': os.getenv('WECHAT_MP_TOKEN'),
}

# ----------- 16. 业务配置 -----------
# 短信服务配置
SMS_CONFIG = {
    'PROVIDER': os.getenv('SMS_PROVIDER', 'aliyun'),
    'VIRTUAL_SMS': os.getenv('VIRTUAL_SMS', 'True').lower() == 'true',
    'SHOW_SMS_IN_DEBUG': DEBUG,
    'TEMPLATES': ALIYUN['SMS_TEMPLATES']
}

# CSRF配置
CSRF_TRUSTED_ORIGINS = [
    f"http://{BASE_DOMAIN}",
    f"http://www.{BASE_DOMAIN}",
    "http://localhost:8080",
]

# ----------- 17. 其他配置 -----------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'