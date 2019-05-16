from rest_framework.permissions import IsAuthenticated
#from rest_framework.viewsets import ModelViewSet
from business.models.message import Message
from business.serializers import MessageSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from business.views.filters import MessageFilter
from rest_framework import views

class MessageViewSet(views.APIView):
    """
    消息：增删改查
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    # 指定筛选类
    filter_class = MessageFilter
    ordering_fields = ('add_time',)

    def get_queryset(self,request):
        #取状态数组
        status = request.POST.getlist('status',[])
        return Message.objects.filter(status__in=status)