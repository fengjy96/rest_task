from rest_framework.generics import ListAPIView
from business.models.reason import Reason
from business.serializers.reason_serializer import ReasonsListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from business.filters import ReasonFilter

class ReasonViewSet(ListAPIView):
    """
    原因：增删改查
    """
    queryset = Reason.objects.all()
    serializer_class = ReasonsListSerializer
    # permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    # 指定筛选类
    filterset_class = ReasonFilter
    ordering = ('-add_time',)
