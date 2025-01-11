import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import logging
from celery.schedules import crontab

# 加载环境变量
load_dotenv(override=True)  # 强制覆盖已存在的环境变量

# ----------- 1. 核心配置 -----------
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ----------- 2. 域名配置 -----------
BASE_DOMAIN = os.getenv('BASE_DOMAIN', 'http://192.168.3.16:8080')  # 修改这里
BACKEND_DOMAIN = os.getenv('BACKEND_DOMAIN', '192.168.3.16:8000')   # 修改这里
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://192.168.3.16:8080') # 修改这里

# 允许访问的主机
ALLOWED_HOSTS = [
    '192.168.3.16',  # 你的局域网 IP
    '192.168.3.16:8080',
    '*',    # 允许所有主机访问
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
]

LOCAL_APPS = [
    'users.apps.UsersConfig',
    'articles.apps.ArticlesConfig',
    'qa.apps.QaConfig',
    'membership.apps.MembershipConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + ['django_celery_beat']

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
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # 添加全局模板目录
        ],
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
            'autocommit': True,
        }
    }
}

# ----------- 7. 缓存配置 -----------
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_DB = os.getenv('REDIS_DB', '1')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'RETRY_ON_TIMEOUT': True,
            'CONNECTION_POOL_KWARGS': {'max_connections': 100},
        }
    }
}

# 使用 Redis 作为 session 后端
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

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
    'EXCEPTION_HANDLER': 'users.utils.handlers.custom_exception_handler',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}

# ----------- 10. CORS配置 -----------
CORS_ALLOWED_ORIGINS = [
    "http://192.168.3.16:8080",
    "http://localhost:8080",
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
            'format': '[%(levelname)s] %(asctime)s %(name)s\n%(message)s\n',
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
        'users': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
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
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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

# 记录阿里云配置加载情况
logger = logging.getLogger('users')
logger.info(f"阿里云配置加载完成:")
logger.info(f"ACCESS_KEY_ID: {ALIYUN['ACCESS_KEY_ID']}")
logger.info(f"SMS_SIGN_NAME: {ALIYUN['SMS_SIGN_NAME']}")
logger.info(f"SMS_TEMPLATES: {ALIYUN['SMS_TEMPLATES']}")

# API 基础URL和证书路径配置
BASE_URL = 'http://127.0.0.1:8000'
CERT_DIR = BASE_DIR / 'keys'

# 支付相关配置
PAYMENT_CONFIG = {
    'alipay': {
        'app_id': '2021000142698861',
        'private_key_path': BASE_DIR / 'keys/alipay/app_private_key.pem',
        'public_key_path': BASE_DIR / 'keys/alipay/alipay_public_key.pem',
        'notify_url': f"https://{BACKEND_DOMAIN}/api/v1/membership/notify/alipay/",
        'return_url': f"https://{BACKEND_DOMAIN}/api/v1/membership/notify/alipay/return/",
        'debug': True,
        'sign_type': 'RSA2',
        'charset': 'utf-8',
        'server_url': 'https://openapi-sandbox.dl.alipaydev.com/gateway.do',
    }
}

# 支付宝配置（简化问）
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
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Celery Beat 配置
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SCHEDULE = {
    'check-membership-expiry': {
        'task': 'membership.tasks.check_membership_expiry',
        'schedule': crontab(hour=9, minute=0),
    },
    'handle-expired-memberships': {
        'task': 'membership.tasks.handle_expired_memberships',
        'schedule': crontab(hour=0, minute=0),
    },
}

# ----------- 16. 服务配置 -----------
# 短信服务配置
SMS_CONFIG = {
    'PROVIDER': os.getenv('SMS_PROVIDER', 'aliyun'),
    'TEMPLATES': ALIYUN['SMS_TEMPLATES'],
    'USE_VIRTUAL_SMS': True,  # 是否使用虚拟短信（测试模式）
    'VIRTUAL_SMS_CODE': '123456'  # 虚拟短信的固定验证码
}

# CSRF配置
CSRF_TRUSTED_ORIGINS = [
    f"http://{BASE_DOMAIN}",
    f"http://www.{BASE_DOMAIN}",
    "http://localhost:8080",
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

# ----------- 20. 日志配置 -----------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# 保日志目录存在
import os
if not os.path.exists(BASE_DIR / 'logs'):
    os.makedirs(BASE_DIR / 'logs')

# ----------- 邮件配置 -----------
# 使用阿里企业邮箱 SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 改为SMTP后端
EMAIL_HOST = 'smtp.qiye.aliyun.com'  # 阿里企业邮箱SMTP服务器
EMAIL_PORT = 465  # 使用SSL端口
EMAIL_USE_SSL = True  # 使用SSL
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'service@popo.work')  # 发件邮箱
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # 从环境变量获取密码
DEFAULT_FROM_EMAIL = 'service@popo.work'  # 默认发件人
EMAIL_TIMEOUT = 5  # 设置超时时间

# API基础URL(开发环境)
API_BASE_URL = os.getenv('API_BASE_URL', 'http://192.168.3.16:8000')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://192.168.3.16:8080')  
# 会员相关URL
MEMBERSHIP_URLS = {
    'renewal': f"{FRONTEND_URL}/membership/renewal",  # 会员续费页面
}

# 支付宝配置
ALIPAY_CONFIG = {
    'DEBUG': True,  # 沙箱环境
    'APP_ID': '2021000142698861',  # 沙箱应用ID
    'NOTIFY_URL': f"{API_BASE_URL}/api/v1/membership/notify/alipay/",  # 异步通知地址
    'RETURN_URL': "http://192.168.3.16:8080/payment/success",  # 直接跳转到前端成功页面
    'FAIL_URL': f"{FRONTEND_URL}/payment/fail",  # 支付失败跳转页面
    'SANDBOX_LOGIN_URL': 'https://open.alipay.com/develop/sandbox/account',  # 沙箱登录地址
    'PRODUCTION_URL': 'https://openapi.alipay.com/gateway.do',
    'PRIVATE_KEY_PATH': os.path.join(BASE_DIR, 'keys', 'alipay', 'app_private_key.pem'),
    'PUBLIC_KEY_PATH': os.path.join(BASE_DIR, 'keys', 'alipay', 'alipay_public_key.pem')
}

# 确保密钥目录存在
ALIPAY_KEYS_DIR = os.path.join(BASE_DIR, 'keys', 'alipay')
if not os.path.exists(ALIPAY_KEYS_DIR):
    os.makedirs(ALIPAY_KEYS_DIR)

# 支付相关URL
PAYMENT_URLS = {
    'SUCCESS_URL': '/payment/success/',  # 支付成功页面
    'FAIL_URL': '/payment/fail/',  # 支付失败页面
}

# 百度文心一言配置
ERNIE_API_KEY = os.getenv('ERNIE_API_KEY')
ERNIE_SECRET_KEY = os.getenv('ERNIE_SECRET_KEY')

# 会员到期提醒配置
MEMBERSHIP_EXPIRY_REMINDER = {
    'DAYS_BEFORE': [7, 3, 1],  # 到期前7天、3天、1天提醒
    'TEMPLATE_ID': 'membership_expiry_reminder',  # 邮件模板ID
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# 允许上传的文件类型
ALLOWED_UPLOAD_IMAGES = ['image/jpeg', 'image/png', 'image/gif']

# 设置缓存异常处理
DJANGO_REDIS_IGNORE_EXCEPTIONS = True
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True