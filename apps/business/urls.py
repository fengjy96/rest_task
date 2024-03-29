from django.urls import path, include

from rest_framework import routers

from business.views import project, task, step, message, reasons, files

router = routers.DefaultRouter()
router.register('art_projects', project.ProjectViewSet, basename='projects')
router.register('project_reject_reason', project.ProjectRejectReasonViewSet, basename='project_reject_reason')
router.register('project_fee', project.ProjectFeeViewSet, basename='project_fee')
router.register('tasks', task.TaskViewSet, basename='tasks')
router.register('task_allocate_reason', task.TaskAllocateReasonViewSet, basename='task_allocate_reason')
router.register('steps', step.StepViewSet, basename='steps')
router.register('messages', message.MessageViewSet, basename='messages')


urlpatterns = [
    path(r'', include(router.urls)),

    ## 项目相关

    # 选择项目负责人
    path(r'project/receivers', project.ProjectReceiverListView.as_view(), name='project_receivers'),
    # 获取所有项目审核员
    path(r'project/auditors', project.ProjectAuditorListView.as_view(), name='project_auditors'),
    # 项目审核提交
    path(r'project/audit/submit', project.ProjectAuditSubmitView.as_view(), name='project_audit_submit'),
    # 项目审核通过
    path(r'project/audit/pass', project.ProjectAuditPassView.as_view(), name='project_audit_pass'),
    # 项目审核驳回
    path(r'project/audit/reject', project.ProjectAuditRejectView.as_view(), name='project_audit_reject'),
    # 项目人员工资成本
    path(r'project/cost/analysis', project.ProjectCostAnalysisView.as_view(), name='project_cost_analysis'),
    # 项目其它费用成本
    path(r'project/fee/cost/analysis', project.ProjectFeeCostAnalysisView.as_view(), name='project_fee_cost_analysis'),
    # 项目成本分析完成
    path(r'project/cost/analysis/finished', project.ProjectCostAnalysisFinishedView.as_view(),name='project_cost_analysis_finished'),
    # 接手项目
    path(r'project/accept', project.ProjectAcceptView.as_view(), name='project_accept'),
    # 拒接项目
    path(r'project/reject', project.ProjectRejectView.as_view(), name='project_reject'),
    # 项目验收提交
    path(r'project/check/submit', project.ProjectCheckSubmitView.as_view(), name='project_check_submit'),
    # 项目验收通过
    path(r'project/check/pass', project.ProjectCheckPassView.as_view(), name='project_check_pass'),
    # 项目验收不通过
    path(r'project/check/reject', project.ProjectCheckRejectView.as_view(), name='project_check_reject'),
    # 判断项目名是否已存在
    path(r'project/name', project.ProjectNameView.as_view(), name='project_name_is_exist'),
    # 判断是否存在项目
    path(r'has_project', project.HasProjectView.as_view(), name='has_project'),
    # 判断项目是否存在任务
    path(r'project/has_task', project.ProjectHasTaskView.as_view(), name='project_has_task'),

    ## 任务相关

    # 接手任务
    path(r'task/accept', task.TaskAcceptView.as_view(), name='task_accept'),
    # 任务拒接
    path(r'task/reject', task.TaskRejectView.as_view(), name='task_reject'),
    # 获取任务负责人
    path(r'task/receivers', task.TaskReceiverView.as_view(), name='task_receivers'),
    # 任务转派
    path(r'task/allocate', task.TaskAllocateView.as_view(), name='task_allocate'),
    # 任务验收提交
    path(r'task/check/submit', task.TaskCheckSubmitView.as_view(), name='task_check_submit'),
    # 任务验收通过
    path(r'task/check/pass', task.TaskCheckPassView.as_view(), name='task_check_pass'),
    # 任务验收不通过
    path(r'task/check/reject', task.TaskCheckRejectView.as_view(), name='task_check_reject'),
    # 判断是否存在文件为空的任务
    # path(r'project/file/check', '', name='project_file_check'),
    # 获取任务的文件或富文本提交信息列表
    path(r'task/log', task.TaskLogsView.as_view(), name='task_log'),
    # 任务发布
    path(r'task/publish', task.TaskPublishView.as_view(), name='task_publish'),
    # 导入任务数据
    path(r'task/import', task.TaskImportView.as_view(), name='task_import'),
    # 判断任务名是否已存在
    path(r'task/name', task.TaskNameView.as_view(), name='task_name_is_exist'),

    ## 步骤相关

    # 步骤进度更新
    path(r'step/progress/update', step.StepProgressUpdateView.as_view(), name='step_progress_update'),
    # 单条步骤进度更新日志
    path(r'step/progress/log', step.StepProgressUpdateLogsView.as_view(), name='step_progress_log'),
    # 步骤进度日志反馈提交
    path(r'step/file/feedback/submit', step.StepLogFileFeedBackUpdateView.as_view(), name='step_log_file_feedback_submit'),
    # 获取步骤进度反馈日志
    path(r'step/file/feedback/log', step.StepLogFileFeedBackLogView.as_view(), name='step_log_file_feedback_log'),

    ## 文件相关

    # 文件上传
    path(r'files/upload', files.UploadFilesView.as_view(),name='files_upload'),
    # 富文件上传
    path(r'rte/files/upload', files.UploadRteFilesView.as_view(),name='rte_files_upload'),
    # 文件删除
    path(r'files/delete', files.DeleteFileView.as_view(), name='files_delete'),
    # 下载文件
    path(r'imageDown', files.FileDownloadView.as_view(),name='file_download'),

    ## 消息相关

    # 消息查询
    path(r'message/update', message.MessageUpdateViewSet.as_view(), name='message_update'),

    ## 原因相关
    path(r'reasons', reasons.ReasonViewSet.as_view(), name='reasons'),
]
