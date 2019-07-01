import django_filters

from configuration.models import task_conf


class TaskStepFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter('name', lookup_expr='icontains')

    class Meta:
        model = task_conf.TaskStep
        fields = ['name', 'task_type', 'task_design_type']
