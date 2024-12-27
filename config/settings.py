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
NGROK_URL = os.getenv('NGROK_URL', 'https://f91a-205-198-122-83.ngrok-free.app')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'spaniel-square-perfectly.ngrok-free.app',
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
    'django_ckeditor_5',
    'simpleui',
]

LOCAL_APPS = [
    'users.apps.UsersConfig',
    'articles.apps.ArticlesConfig',
    'qa.apps.QaConfig',
    'membership.apps.MembershipConfig',
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
        'NAME': os.getenv('DB_NAME', 'flybird'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET default_storage_engine=INNODB, time_zone='+8:00'",
        }
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
    'users.backends.PhoneModelBackend',
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
    'EXCEPTION_HANDLER': 'users.utils.handlers.custom_exception_handler',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}

# ----------- 10. CORS配置 -----------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://spaniel-square-perfectly.ngrok-free.app",
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
            'format': '\n[%(levelname)s] %(asctime)s %(name)s\n%(message)s\n',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'membership': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'alipay': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
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
# 阿里配置
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

# API 基础URL和证书路径配置
BASE_URL = 'http://127.0.0.1:8000'
CERT_DIR = BASE_DIR / 'keys'

# 支付相关配置
PAYMENT_CONFIG = {
    'alipay': {
        'app_id': '2021000142698861',
        'private_key_path': BASE_DIR / 'keys/alipay/app_private_key.pem',
        'public_key_path': BASE_DIR / 'keys/alipay/alipay_public_key.pem',
        'notify_url': f"http://localhost:8000/api/v1/membership/notify/alipay/",
        'return_url': f"http://localhost:8000/api/v1/membership/notify/alipay/return/",
        'debug': True,
        'sign_type': 'RSA2',
        'charset': 'utf-8',
        'server_url': 'https://openapi-sandbox.dl.alipaydev.com/gateway.do',
    }
}

# 支付宝配置（简化访问）
ALIPAY_APP_ID = PAYMENT_CONFIG['alipay']['app_id']
ALIPAY_NOTIFY_URL = PAYMENT_CONFIG['alipay']['notify_url']
ALIPAY_RETURN_URL = PAYMENT_CONFIG['alipay']['return_url']
ALIPAY_SERVER_URL = PAYMENT_CONFIG['alipay']['server_url']

# ----------- Celery配置 -----------
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# 解决警告信息
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Celery定时任务
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'check-expired-memberships': {
        'task': 'membership.tasks.check_expired_memberships',
        'schedule': crontab(hour='*/1'),
    },
    'send-expiration-reminder': {
        'task': 'membership.tasks.send_expiration_reminder',
        'schedule': crontab(hour='9', minute='0'),
    },
    'cancel-expired-orders': {
        'task': 'membership.tasks.cancel_expired_orders',
        'schedule': crontab(minute='*/30'),
    },
}

# ----------- 16. 服务配置 -----------
# 短��服务配置
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
    "https://spaniel-square-perfectly.ngrok-free.app",
]

# ----------- 17. 其他配置 -----------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ----------- 18. CKEditor 5 配置 -----------
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                   'bulletedList', 'numberedList', 'blockQuote', '|',
                   'imageUpload', 'insertTable', 'mediaEmbed', '|',
                   'code', 'codeBlock', '|',
                   'sourceEditing'],
        'height': '400px',
        'width': '100%',
    },
}

CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
CKEDITOR_5_UPLOAD_PATH = "uploads/"

# ----------- 19. SimpleUI配置 -----------
SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menu_display': ['认证和授权', '用户管理', '文章管理', '问答管理'],
    'dynamic': True,
    'menus': [
        {
            'name': '用户管理',
            'icon': 'fas fa-user-circle',
            'models': [
                {
                    'name': '用户列表',
                    'icon': 'fas fa-user',
                    'url': 'users/user/'
                }
            ]
        },
        {
            'name': '文章管理',
            'icon': 'fas fa-book',
            'models': [
                {
                    'name': '文章分类',
                    'icon': 'fas fa-tags',
                    'url': 'articles/category/'
                },
                {
                    'name': '文章列表',
                    'icon': 'fas fa-file-alt',
                    'url': 'articles/article/'
                },
                {
                    'name': '评论管理',
                    'icon': 'fas fa-comments',
                    'url': 'articles/comment/'
                }
            ]
        },
        {
            'name': '问答管理',
            'icon': 'fas fa-question-circle',
            'models': [
                {
                    'name': '问题列表',
                    'icon': 'fas fa-question',
                    'url': 'qa/question/'
                },
                {
                    'name': '回答列表',
                    'icon': 'fas fa-reply',
                    'url': 'qa/answer/'
                },
                {
                    'name': '评论管理',
                    'icon': 'fas fa-comments',
                    'url': 'qa/comment/'
                }
            ]
        }
    ]
}

SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
SIMPLEUI_HOME_QUICK = True
SIMPLEUI_HOME_ACTION = True
SIMPLEUI_DEFAULT_THEME = 'admin.lte.css'
SIMPLEUI_LOGO = '/static/admin/img/logo.png'

SIMPLEUI_DEFAULT_ICON = False
SIMPLEUI_ICON = {
    '认证和授权': 'fas fa-shield-alt',
    '用户管理': 'fas fa-users-cog',
    '文章管理': 'fas fa-newspaper',
    '问答管理': 'fas fa-comments',
}

# ----------- 20. 日志配置 -----------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '\n[%(levelname)s] %(asctime)s %(name)s\n%(message)s\n',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'membership': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'alipay': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# 确保日志目录存在
import os
if not os.path.exists(BASE_DIR / 'logs'):
    os.makedirs(BASE_DIR / 'logs')