from .celery import *
import os, sys, datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 密钥，用于 hash 算法
SECRET_KEY = 'x^*!*=ao%3t2ay-0zw-21!&oz=%4gwu0=&*omt@zi%3t^dyd8!'

# 是否开启 DEBUDG 模式（生产环境中需要关闭）
DEBUG = True

# 一个字符串列表，用来表示 Django 站点可以服务的 host/domain
# 这是一个安全措施，用来预防 HTTP Host header attacks
ALLOWED_HOSTS = ['*']

# 在 Django 项目中需要安装的应用列表
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'channels',
    # 应用：解决跨域问题
    'corsheaders',
    # 应用：
    'django_filters',
    # 应用：基于角色的访问权限控制
    'rbac',
    # 应用：配置管理数据库
    'cmdb',
    # 应用：部署
    'deployment',
    # 应用：项目管理系统业务
    'business',
    # 应用：积分
    'points',
    # 应用：项目管理系统业务配置
    'configuration',
]

# 中间件
MIDDLEWARE = [
    # 跨域
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 操作记录
    'simple_history.middleware.HistoryRequestMiddleware',
]

# CORS 跨域设置
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'rest_xops.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'rest_xops.wsgi.application'

# 数据库相关配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rest_xops',
        'HOST': '192.168.1.110',
        'USER': 'root',
        'PASSWORD': 'mikai',
        'PORT': '3306',
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB;'}
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    # 'rest_framework.authentication.BasicAuthentication',#
    # 'rest_framework.authentication.SessionAuthentication',#
    # ),
    # 自定义异常处理
    'EXCEPTION_HANDLER': 'apps.common.custom.xops_exception_handler',
    # 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',# 过滤功能
    # 'rest_framework.filters.SearchFilter',  # 搜索功能
    # 'rest_framework.filters.OrderingFilter',  # 排序功能
    # ),
}

# jwt setting
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=3),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

## redis 数据库相关配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None

# django-channels配置
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# 配置 ASGI
ASGI_APPLICATION = "rest_xops.routing.application"

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# 语言默认是 en-us，这里改为中文
LANGUAGE_CODE = 'zh-hans'

# 一个字符串，用来指定存储到数据库中的时区
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# 数据库存储使用时间，设置为 True 的话，时间会被存为 UTC 的时间
USE_TZ = False

# 此处重载是为了使我们的 UserProfile 生效
AUTH_USER_MODEL = 'rbac.UserProfile'

# 静态文件存放路径
STATIC_URL = '/static/'

# 资源文件存放路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# yml 配置文件存放的目录
YML_CONF_DIR = os.path.join(BASE_DIR, 'conf')

# 部署管理工作区地址
WORKSPACE = '/tmp/workspace/'

# 日志
BASE_LOG_DIR = os.path.join(BASE_DIR, 'logs')

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(levelname)s]''[%(filename)s:%(lineno)d][%(message)s]'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s]%(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_LOG_DIR, "info_xops.log"),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 3,
            'formatter': 'simple',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_LOG_DIR, "err_xops.log"),
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'info': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True,
        },
        'warn': {
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': True,
        },
        'error': {
            'handlers': ['error'],
            'level': 'ERROR',
        },
    },
}
