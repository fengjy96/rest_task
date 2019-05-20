from django.urls import path, include
from rest_framework import routers
from business.views import task
from business.views.project import ProjectViewSet, ProjectRejectReasonViewSet, ProjectFeeViewSet
from business.views import project
from business.views.task import TaskViewSet, TaskAllocateReasonViewSet
from business.views.step import StepViewSet
from business.views import files
from business.views import message
# from business.views import step

router = routers.DefaultRouter()
router.register('art_projects', ProjectViewSet, basename='projects')
router.register('project_reject_reason', ProjectRejectReasonViewSet, basename='project_reject_reason')
router.register('project_fee', ProjectFeeViewSet, basename='project_fee')
router.register('tasks', TaskViewSet, basename='tasks')
router.register('task_allocate_reason', TaskAllocateReasonViewSet, basename='task_allocate_reason')
router.register('steps', StepViewSet, basename='steps')

urlpatterns = [
    # API
    path(r'api/v1/', include(router.urls)),
    # 选择项目负责人
    path(r'api/v1/project/receivers', project.ProjectReceiverListView.as_view(), name='project_receivers'),
    # 获取所有项目审核员
    path(r'api/v1/project/auditors', project.ProjectAuditorListView.as_view(), name='project_auditors'),
    # 判断是否存在文件为空的任务
    #path(r'api/v1/project/file/check', '', name='project_file_check'),
    # 项目审核提交
    path(r'api/v1/project/audit/submit', project.ProjectAuditSubmitView.as_view(), name='project_audit_submit'),
    # 项目审核通过
    path(r'api/v1/project/audit/pass', project.ProjectAuditPassView.as_view(), name='project_audit_pass'),
    # 项目审核驳回
    path(r'api/v1/project/audit/reject', project.ProjectAuditRejectView.as_view(), name='project_audit_reject'),
    # 项目成本分析
    path(r'api/v1/project/cost/analysis', project.ProjectCostAnalysisView.as_view(), name='project_cost_analysis'),
    # 接手项目
    path(r'api/v1/project/accept', project.ProjectAcceptView.as_view(), name='project_accept'),
    # 接手任务
    path(r'api/v1/task/accept', task.TaskAcceptView.as_view(), name='task_accept'),
    # 获取任务负责人
    path(r'api/v1/task/receivers', task.TaskReceiverView.as_view(), name='task_receivers'),
    # 任务转派
    path(r'api/v1/task/allocate', task.TaskAllocateView.as_view(), name='task_allocate'),
    # 文件上传
    #path(r'api/v1/imageUpload', files.FileUploadView.as_view(),name='file_upload'),
    path(r'api/v1/imageUpload', files.AddStepLogFiles.as_view(),name='file_upload'),
    # 下载文件
    path(r'api/v1/imageDown', files.FileDownloadView.as_view(),name='file_download'),
    # 文件查询
    path(r'api/v1/files', files.FilesListViewSet.as_view(),name='files'),
    # 消息查询
    path(r'api/v1/messages', message.MessageViewSet.as_view(), name='messages'),
]
