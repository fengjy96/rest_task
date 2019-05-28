from django.urls import path,include
from rest_framework import routers

from deployment.views import project, deploy, applog


router = routers.SimpleRouter()

# 项目相关
router.register(r'projects', project.ProjectViewSet, base_name="projects")
# 部署记录相关
router.register(r'deploy/records', deploy.DeployRecordViewSet, base_name="deploy_record")

urlpatterns = [
    path(r'api/', include(router.urls)),
    # 部署执行相关
    path(r'api/deploy/excu/', deploy.DeployView.as_view(), name='deploy'),
    # 部署版本相关
    path(r'api/deploy/ver/', deploy.VersionView.as_view(), name='version'),
    # 远程应用日志相关
    path(r'api/deploy/applog/', applog.AppLogView.as_view(), name='applog'),
    # 项目拷贝相关
    path(r'api/project/copy/', project.ProjectCopy.as_view(), name='project_copy')
]