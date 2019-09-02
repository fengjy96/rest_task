from django_filters import rest_framework as filters

from business.models.project import Project
from business.models.task import Task
from business.models.step import Step
from business.models.files import Files
from business.models.message import Message
from business.models.reason import Reason


class ProjectFilter(filters.FilterSet):
    """
    自定义过滤器需要继承 django_filters.rest_framework.FilterSet 类来写

    定义进行过滤的参数，CharFilter 是过滤参数的类型，过滤器参数类型还有很多，包括
    BooleanFilter，ChoiceFilter，DateFilter，NumberFilter，RangeFilter.. 等等
    field_name 为筛选的参数名，需要和你 model 中的一致，lookup_expr 为筛选参数的条件
    例如 icontains 为包含，忽略大小写，例如 NumberFilter 则可以有 gte，gt，lte，lt，
    year__gt，year__lt 等
    """
    name = filters.CharFilter('name', lookup_expr='icontains')
    style = filters.CharFilter('style', lookup_expr='icontains')
    customer = filters.CharFilter('customer', lookup_expr='icontains')

    class Meta:
        """
        指定筛选的 model 和筛选的参数，其中筛选的参数在前面设置了筛选条件，则根据筛选条件来执行，
        如果未指定筛选条件，则按照精确查询来执行
        """
        model = Project
        fields = ['name', 'style', 'customer', 'is_finished', 'audit_status', 'receiver', 'sender', 'auditor',
                  'audit_status', 'is_active', 'receive_status']


class TaskFilter(filters.FilterSet):
    name = filters.CharFilter('name', lookup_expr='icontains')

    class Meta:
        model = Task
        fields = ['name', 'receiver', 'sender', 'project', 'receive_status', 'audit_status', 'is_published', 'superior']


class StepFilter(filters.FilterSet):
    class Meta:
        model = Step
        fields = ['task', 'sender']


class FilesFilter(filters.FilterSet):
    class Meta:
        model = Files
        fields = ['tasklog', 'steplog']


class MessageFilter(filters.FilterSet):
    class Meta:
        model = Message
        fields = ['receiver']


class ReasonFilter(filters.FilterSet):
    class Meta:
        model = Reason
        fields = ['type_id', 'link_id']
