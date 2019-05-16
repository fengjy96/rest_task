from django.urls import path, include

from rest_framework import routers

from business.views import project
from business.views import task
from business.views import step
from business.views.message import MessageViewSet
from business.views.project import ProjectViewSet, ProjectRejectReasonViewSet, ProjectFeeViewSet
from business.views import project
from business.views.task import TaskViewSet, TaskAllocateReasonViewSet
from business.views.step import StepViewSet
from business.views import files

router = routers.DefaultRouter()
router.register('project', ProjectViewSet, basename='project')
router.register('project_reject_reason', ProjectRejectReasonViewSet, basename='project_reject_reason')
router.register('project_fee', ProjectFeeViewSet, basename='project_fee')
router.register('task', TaskViewSet, basename='task')
router.register('task_allocate_reason', TaskAllocateReasonViewSet, basename='task_allocate_reason')
router.register('step', StepViewSet, basename='step')

urlpatterns = [
    # API
    path(r'api/v1/', include(router.urls)),
    # 1.选择项目负责人
    path(r'api/v1/project/receiver', project.ProjectReceiverListView.as_view(), name='project_receiver'),
    # 2.判断是否存在文件为空的任务
    #path(r'api/v1/project/file/check', '', name='project_file_check'),
    # 3.项目审核提交
    path(r'api/v1/project/audit/submit', project.ProjectAuditSubmitView.as_view(), name='project_audit_submit'),
    # 4.项目审核通过
    path(r'api/v1/project/audit/pass', project.ProjectAuditPassView.as_view(), name='project_audit_pass'),
    # 5.项目审核驳回
    path(r'api/v1/project/audit/reject', project.ProjectAuditRejectView.as_view(), name='project_audit_reject'),
    # 6.项目成本分析
    path(r'api/v1/project/cost/analysis', project.ProjectCostAnalysisView.as_view(), name='project_cost_analysis'),
    # 7.接手项目
    path(r'api/v1/project/accept', project.ProjectAcceptView.as_view(), name='project_accept'),
    # 8.接手任务
    path(r'api/v1/task/accept', task.TaskAcceptView.as_view(), name='task_accept'),
    # 9.选择任务负责人
    path(r'api/v1/task/receiver', task.TaskSelectReceiverView.as_view(), name='task_receiver'),
    # 10.任务转派
    path(r'api/v1/task/allocate', task.TaskAllocateView.as_view(), name='task_allocate'),
    # 16.根据条件查询项目信息
    path(r'api/v1/project/condition', project.ProjectListView.as_view(), name='project_condition'),
    # 17.文件上传
    #path(r'api/v1/imageUpload', files.FileUploadView.as_view(),name='file_upload'),
    path(r'api/v1/imageUpload', files.AddStepLogFiles.as_view(),name='file_upload'),
    # 18 下载文件
    path(r'api/v1/imageDown', files.FileDownloadView.as_view(),name='file_download'),
    # 19 文件查询
    path(r'api/v1/files', files.FilesListViewSet.as_view(),name='files'),
]
