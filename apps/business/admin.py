from django.contrib import admin

from business.models.project import Project, ProjectFee, ProjectRejectReason
from business.models.task import Task, TaskAllocateReason
from business.models.step import Step, StepRejectReason


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['company', 'name', 'style', 'progress', 'points', 'is_active',
                    'is_finished', 'customer', 'sender', 'receiver', 'receive_status', 'auditor',
                    'audit_status',
                    'begin_time', 'end_time', 'add_time', 'modify_time']
    list_filter = ['company', 'name', 'style', 'progress', 'points', 'is_active',
                   'is_finished', 'customer', 'sender', 'receiver', 'receive_status', 'auditor',
                   'audit_status',
                   'begin_time', 'end_time', 'add_time', 'modify_time']
    search_fields = ['company', 'name', 'style', 'progress', 'points', 'is_active',
                     'is_finished', 'customer', 'sender', 'receiver', 'receive_status', 'auditor',
                     'audit_status',
                     'begin_time', 'end_time', 'add_time', 'modify_time']


class ProjectFeeAdmin(admin.ModelAdmin):
    list_display = ['company', 'project', 'name', 'value']
    list_filter = ['company', 'project', 'name', 'value']
    search_fields = ['company', 'project', 'name', 'value']


class ProjectRejectReasonAdmin(admin.ModelAdmin):
    list_display = ['project', 'reason', 'add_time']
    list_filter = ['project', 'reason', 'add_time']
    search_fields = ['project', 'reason', 'add_time']


class TaskAdmin(admin.ModelAdmin):
    list_display = ['company', 'name', 'task_type', 'content', 'progress', 'task_priority',
                    'task_quality',
                    'begin_time', 'end_time', 'task_assessment', 'comments', 'points', 'memo',
                    'project', 'sender', 'receive_status', 'auditor', 'audit_status',
                    'is_active',
                    'is_finished', 'add_time', 'modify_time']
    list_filter = ['company', 'name', 'task_type', 'content', 'progress', 'task_priority',
                   'task_quality',
                   'begin_time', 'end_time', 'task_assessment', 'comments', 'points', 'memo',
                   'project', 'sender', 'receive_status', 'auditor', 'audit_status',
                   'is_active',
                   'is_finished', 'add_time', 'modify_time']
    search_fields = ['company', 'name', 'task_type', 'content', 'progress', 'task_priority',
                     'task_quality',
                     'begin_time', 'end_time', 'task_assessment', 'comments', 'points', 'memo',
                     'project', 'sender', 'receive_status', 'auditor', 'audit_status',
                     'is_active',
                     'is_finished', 'add_time', 'modify_time']


class TaskAllocateReasonAdmin(admin.ModelAdmin):
    list_display = ['task', 'reason', 'transfer_nums', 'sender', 'receiver', 'add_time']
    list_filter = ['task', 'reason', 'transfer_nums', 'sender', 'receiver', 'add_time']
    search_fields = ['task', 'reason', 'transfer_nums', 'sender', 'receiver', 'add_time']


class StepAdmin(admin.ModelAdmin):
    list_display = ['company', 'task', 'name', 'index', 'task_design_type', 'is_active', 'is_finished',
                    'sender', 'receiver', 'receive_status', 'auditor', 'audit_status',
                    'begin_time',
                    'end_time', 'add_time', 'modify_time']
    list_filter = ['company', 'task', 'name', 'index', 'task_design_type', 'is_active', 'is_finished',
                   'sender', 'receiver', 'receive_status', 'auditor', 'audit_status',
                   'begin_time',
                   'end_time', 'add_time', 'modify_time']
    search_fields = ['company', 'task', 'name', 'index', 'task_design_type', 'is_active', 'is_finished',
                     'sender', 'receiver', 'receive_status', 'auditor', 'audit_status',
                     'begin_time',
                     'end_time', 'add_time', 'modify_time']


class StepRejectReasonAdmin(admin.ModelAdmin):
    list_display = ['step', 'reason', 'transfer_nums', 'sender', 'receiver', 'add_time']
    list_filter = ['step', 'reason', 'transfer_nums', 'sender', 'receiver', 'add_time']
    search_fields = ['step', 'reason', 'transfer_nums', 'sender', 'receiver', 'add_time']


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectFee, ProjectFeeAdmin)
admin.site.register(ProjectRejectReason, ProjectRejectReasonAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskAllocateReason, TaskAllocateReasonAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(StepRejectReason, StepRejectReasonAdmin)
