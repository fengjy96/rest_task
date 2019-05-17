import django_filters
from business.models.project import Project
from business.models.task import Task
from business.models.step import Step
from business.models.files import Files
from business.models.message import Message

# 自定义过滤器需要继承 django_filters.rest_framework.FilterSet 类来写
class ProjectFilter(django_filters.rest_framework.FilterSet):
    # 定义进行过滤的参数，CharFilter 是过滤参数的类型，过滤器参数类型还有很多，包括
    # BooleanFilter，ChoiceFilter，DateFilter，NumberFilter，RangeFilter..等等
    # field_name 为筛选的参数名，需要和你 model 中的一致，lookup_expr 为筛选参数的条件
    # 例如 icontains 为 忽略大小写包含，例如 NumberFilter 则可以有 gte，gt，lte，lt，
    # year__gt，year__lt 等
    name = django_filters.CharFilter('name', lookup_expr='icontains')
    style = django_filters.CharFilter('style', lookup_expr='icontains')
    customer = django_filters.CharFilter('customer', lookup_expr='icontains')
    # 指定筛选的 model 和筛选的参数，其中筛选的参数在前面设置了筛选条件，则根据筛选条件来执行，
    # 如果为指定筛选条件，则按照精确查询来执行
    class Meta:
        model = Project
        fields = ['name', 'style',  'customer', 'is_finished', 'receiver_id', 'sender_id', 'auditor_id']


class TaskFilter(django_filters.rest_framework.FilterSet):
     name = django_filters.CharFilter('name', lookup_expr='icontains')
     class Meta:
         model = Task
         fields = ['name', 'is_finished', 'receiver_id', 'sender_id', 'project_id']


class StepFilter(django_filters.rest_framework.FilterSet):
     class Meta:
         model = Step
         fields = ['task_id','sender_id']


class FilesFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Files
        fields = ['task_id', 'steplog_id']

class MessageFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Message
        fields = ['receiver_id']
