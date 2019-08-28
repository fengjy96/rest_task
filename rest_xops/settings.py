from .celery import *
import os, sys, datetime

# Project Base Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path --> A list of strings that specifies the search path for modules
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 密钥，用于 hash 算法
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x^*!*=ao%3t2ay-0zw-21!&oz=%4gwu0=&*omt@zi%3t^dyd8!'

# 是否开启 DEBUG 模式（生产环境中需要关闭）
DEBUG = True

# 一个字符串列表，用来表示 Django 站点可以服务的 host/domain
# 这是一个安全措施，用来预防 HTTP Host header attacks
ALLOWED_HOSTS = ['*']

# 本地 ip
HOST = '127.0.0.1'

## 在 Django 项目中需要安装的应用列表
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # 应用：用于实现 websocket
    # 'channels',
    # 应用：解决跨域问题
    'corsheaders',
    # 应用：包括一个 DjangoFilterBackend 类，它支持 REST 框架的高度可定制的字段过滤
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

## 中间件
MIDDLEWARE = [
    # 跨域中间件
    'corsheaders.middleware.CorsMiddleware',
    # 安全中间件：一些安全设置，比如 XSS 脚本过滤
    'django.middleware.security.SecurityMiddleware',
    # 会话中间件：加入这个中间件，会在数据库中生成一个 django_session 的表
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 通用中间件：会处理一些 URL，如为 URL 加 www 前缀，或在 URL 尾部加反斜线
    'django.middleware.common.CommonMiddleware',
    # 跨域请求伪造中间件：防 CSRF 攻击
    'django.middleware.csrf.CsrfViewMiddleware',
    # 认证中间件：会在每个 HttpRequest 对象到达 view 之前添加当前登录用户的 user 属性
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 消息中间件：展示一些后台信息给前端页面
    'django.contrib.messages.middleware.MessageMiddleware',
    # 防点击劫持中间件：防止通过浏览器页面跨Frame出现clickjacking（欺骗点击）攻击出现
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 操作记录中间件
    'simple_history.middleware.HistoryRequestMiddleware',
]

# CORS 跨域设置
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'rest_xops.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

## 数据库相关配置
DATABASES = {
    # 指定默认的数据库
    'default': {
        # 数据库引擎
        'ENGINE': 'django.db.backends.mysql',
        # 数据库名
        'NAME': 'rest_xops',
        'HOST': HOST,
        'USER': 'root',
        'PASSWORD': 'mysql',
        # 内网 centos mysql 密码
        # 'PASSWORD': 'mikai',
        'PORT': '3306',
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB; SET foreign_key_checks = 0;'}
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
    ## 版本配置
    # 默认版本类
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    # 允许的版本
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    # 版本参数
    'VERSION_PARAM': 'version',

    ## 指定默认的认证类
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # jwt 认证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 基本认证
        'rest_framework.authentication.BasicAuthentication',
        # 会话认证
        'rest_framework.authentication.SessionAuthentication',
    ),
    ## 自定义异常处理
    'EXCEPTION_HANDLER': 'apps.common.custom.xops_exception_handler',
    ## 定制字段过滤
    'DEFAULT_FILTER_BACKENDS': (
        # 过滤功能
        # 'django_filters.rest_framework.DjangoFilterBackend',
        # 搜索功能
        # 'rest_framework.filters.SearchFilter',
        # 排序功能：OrderingFilter 类支持简单的查询参数控制结果排序
        # 'rest_framework.filters.OrderingFilter',
    ),
    ## 默认的渲染器类
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    #     'rest_framework.renderers.BrowsableAPIRenderer',
    # ),
}

## jwt 设置
JWT_AUTH = {
    # jwt token 有效期：指定为 3 天
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=3),
    # jwt 认证头前缀
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

## redis 数据库相关设置
REDIS_HOST = HOST
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None

# django-channels 配置
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
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'standard': {
#             'format': '[%(asctime)s][%(levelname)s]''[%(filename)s:%(lineno)d][%(message)s]'
#         },
#         'simple': {
#             'format': '[%(levelname)s][%(asctime)s]%(message)s'
#         },
#     },
#     'handlers': {
#         'default': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(BASE_LOG_DIR, "info_xops.log"),
#             'maxBytes': 1024 * 1024 * 50,
#             'backupCount': 3,
#             'formatter': 'simple',
#             'encoding': 'utf-8',
#         },
#         'error': {
#             'level': 'ERROR',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(BASE_LOG_DIR, "err_xops.log"),
#             'backupCount': 5,
#             'formatter': 'standard',
#             'encoding': 'utf-8',
#         },
#     },
#     'loggers': {
#         'info': {
#             'handlers': ['default'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#         'warn': {
#             'handlers': ['default'],
#             'level': 'WARNING',
#             'propagate': True,
#         },
#         'error': {
#             'handlers': ['error'],
#             'level': 'ERROR',
#         },
#     },
# }

# 将 sql 语句打印到控制台

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
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
       'django.db.backends': {
           'handlers': ['console'],
           'propagate': True,
           'level': 'DEBUG',
       }
    },
}

# FILE_UPLOAD_MAX_MEMORY_SIZE = 50*1024*1024

# ################## 默认文件上传配置 ########################
from django.core.files.uploadhandler import MemoryFileUploadHandler
from django.core.files.uploadhandler import TemporaryFileUploadHandler

# List of upload handler classes to be applied in order.
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# Maximum size, in bytes, of a request before it will be streamed to the
# file system instead of into memory.
# 允许内存中上传文件的大小
#   合法：InMemoryUploadedFile对象（写在内存）         -> 上传文件小于等于 FILE_UPLOAD_MAX_MEMORY_SIZE
# 不合法：TemporaryUploadedFile对象（写在临时文件）     -> 上传文件大于    FILE_UPLOAD_MAX_MEMORY_SIZE 且 小于 DATA_UPLOAD_MAX_MEMORY_SIZE

FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # i.e. 2.5 MB

# Maximum size in bytes of request data (excluding file uploads) that will be
# read before a SuspiciousOperation (RequestDataTooBig) is raised.
# 允许上传内容的大小（包含文件和其他请求内容）
DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400  # i.e. 25 MB

# Maximum number of GET/POST parameters that will be read before a
# SuspiciousOperation (TooManyFieldsSent) is raised.
# 允许的上传文件数
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# Directory in which upload streamed files will be temporarily saved. A value of
# `None` will make Django use the operating system's default temporary directory
# (i.e. "/tmp" on *nix systems).
# 临时文件夹路径
FILE_UPLOAD_TEMP_DIR = None

# The numeric mode to set newly-uploaded files to. The value should be a mode
# you'd pass directly to os.chmod; see https://docs.python.org/3/library/os.html#files-and-directories.
# 文件权限
FILE_UPLOAD_PERMISSIONS = None

# The numeric mode to assign to newly-created directories, when uploading files.
# The value should be a mode as you'd pass to os.chmod;
# see https://docs.python.org/3/library/os.html#files-and-directories.
# 文件夹权限
FILE_UPLOAD_DIRECTORY_PERMISSIONS = None
