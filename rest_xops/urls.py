from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # 角色相关
    path(r'', include('rbac.urls')),
    # 配置相关
    path(r'', include('cmdb.urls')),
    # 部署相关
    path(r'', include('deployment.urls')),
    # 业务相关
    path(r'', include('business.urls')),
    # 积分相关
    path(r'', include('points.urls')),
    # 业务配置相关
    path(r'', include('configuration.urls')),
    # 接口文档
    path('docs/', include_docs_urls()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
