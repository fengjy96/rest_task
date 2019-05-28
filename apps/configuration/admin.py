from django.contrib import admin

from configuration.models import (
    TaskPriority, TaskQuality, TaskType, TaskDesignType, TaskAssessment, TaskStep, Salary, Skill)


class TaskPriorityAdmin(admin.ModelAdmin):
    list_display = ['name', 'index', 'company', 'weight']
    list_filter = ['name', 'index', 'company', 'weight']
    search_fields = ['name', 'index', 'company', 'weight']


class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ['company', 'name', 'index', 'is_active']
    list_filter = ['company', 'name', 'index', 'is_active']
    search_fields = ['company', 'name', 'index', 'is_active']


class TaskQualityAdmin(admin.ModelAdmin):
    list_display = ['name', 'index', 'company', 'weight']
    list_filter = ['name', 'index', 'company', 'weight']
    search_fields = ['name', 'index', 'company', 'weight']


class TaskAssessmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'index', 'company', 'weight', 'is_active']
    list_filter = ['name', 'index', 'company', 'weight', 'is_active']
    search_fields = ['name', 'index', 'company', 'weight', 'is_active']


class TaskDesignTypeAdmin(admin.ModelAdmin):
    list_display = ['company', 'task_type', 'name', 'index', 'is_active']
    list_filter = ['company', 'task_type', 'name', 'index', 'is_active']
    search_fields = ['company', 'task_type', 'name', 'index', 'is_active']


class TaskStepAdmin(admin.ModelAdmin):
    list_display = ['company', 'name', 'task_type', 'task_design_type', 'is_active']
    list_filter = ['company', 'name', 'task_type', 'task_design_type', 'is_active']
    search_fields = ['company', 'name', 'task_type', 'task_design_type', 'is_active']


class SalaryAdmin(admin.ModelAdmin):
    list_display = ['user', 'wage', 'is_active']
    list_filter = ['user', 'wage', 'is_active']
    search_fields = ['user', 'wage', 'is_active']


class SkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'task_type', 'is_active']


admin.site.register(TaskPriority, TaskPriorityAdmin)
admin.site.register(TaskType, TaskTypeAdmin)
admin.site.register(TaskQuality, TaskQualityAdmin)
admin.site.register(TaskAssessment, TaskAssessmentAdmin)
admin.site.register(TaskDesignType, TaskDesignTypeAdmin)
admin.site.register(TaskStep, TaskStepAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(Skill, SkillAdmin)
