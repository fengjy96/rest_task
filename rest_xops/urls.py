from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # 角色相关
    re_path(r'api/(?P<version>(v1|v2))/', include('rbac.urls')),
    # 配置相关
    re_path(r'api/(?P<version>(v1|v2))/', include('cmdb.urls')),
    # 部署相关
    re_path(r'api/(?P<version>(v1|v2))/', include('deployment.urls')),
    # 业务相关
    re_path(r'api/(?P<version>(v1|v2))/', include('business.urls')),
    # 积分相关
    re_path(r'api/(?P<version>(v1|v2))/', include('points.urls')),
    # 业务配置相关
    re_path(r'api/(?P<version>(v1|v2))/', include('configuration.urls')),
    # 接口文档
    path('docs/', include_docs_urls()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
