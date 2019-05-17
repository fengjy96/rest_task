from rest_framework import views
from utils.basic import MykeyResponse
from rest_framework import status
from django.http import FileResponse
from business.models.files import Files,ProgressTexts,FeedBacks,FeedBackTexts
from rest_framework.viewsets import ModelViewSet
from business.serializers import FilesSerializer,FilesListSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from business.views.filters import FilesFilter
#from business.views.forms import UploadFileForm
from rest_framework.generics import ListAPIView
from django.conf import settings
from business.models.steplog import StepLog,FeedBackLog
import os
import uuid

class FilesViewSet(ModelViewSet):
    """
    文件：增删改查
    """
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    # permission_classes = (IsAuthenticated,)

class FilesListViewSet(ListAPIView):
    """
    文件：增删改查
    """
    queryset = Files.objects.all()
    serializer_class = FilesListSerializer
    # permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    # 指定筛选类
    filter_class = FilesFilter
    ordering_fields = ('id',)

    def get_queryset(self):
        # 文件状态为激活
        is_active = 1

        return Files.objects.filter(is_active=is_active)


class StepLogFilesListViewSet(ListAPIView):
    """
    文件：查询反馈信息
    """
    pass


class AddStepLogFiles(views.APIView):
    """
    上传多个文件
    """
    def post(self, request):
        try:
         # 步骤标识
         step_id = request.data.get('step_id')
         # 标题
         title = request.data.get('title')
         # 进度
         progress = request.data.get('progress')
         # 备注
         memo = request.data.get('memo')
         # 类型
         type = request.data.get('type')
         # 内容
         content = request.data.get('content')

         #增加步骤日志
         if step_id is not None and title is not None and progress is not None and memo is not None:
             steplog = StepLog(step_id=step_id,title=title,progress=progress,memo=memo)
             steplog.save()

             # 如果存在富文本,则先添加富文本
             if type is not None and content is not None:
                 if type == 0:
                     progresstexts = ProgressTexts(steplog_id=steplog.id,content=content)
                     progresstexts.save()

             #获取用户上传的文件,保存到服务器,再添加到数据库
             files = request.files.getlist('file')
             #判断文件列表是否存在文件
             if len(files) > 0:
                 #判断上传路径是否存在，不存在则创建
                 if not os.path.exists(settings.MEDIA_ROOT):
                     os.makedirs(settings.MEDIA_ROOT)
                 #遍历用户上传的文件列表
                 upload_files = []
                 for file in files:
                     #获取文件反缀名
                     extension = os.path.splitext(file.name)[1]
                     #通过uuid重命名上传的文件
                     filename = '{}{}'.format(uuid.uuid4(),extension)
                     #构建文件路径
                     file_path = '{}/{}'.format(settings.MEDIA_ROOT,filename)
                     #将上传的文件路径存储到upload_files中
                     #注意这样要构建相对路径MEDIA_URL+filename,这里可以保存到数据库
                     upload_files.append('{}{}'.format(settings.MEDIA_URL,filename))
                     #保存文件
                     with open(file_path,'wb') as f:
                         for c in file.chunks():
                             f.write(c)
                         f.close()

                     #增加文件
                     file_ = Files(steplog_id=steplog.id,name=filename,path=file_path)
                     file_.save()

        except Exception as e:
           return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')

        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')



class AddFeeBackLogFiles(views.APIView):
    """
    上传多个文件
    """
    def post(self, request):
        try:
         # 步骤标识
         file_id = request.data.get('file_id')
         # 标题
         title = request.data.get('title')
         # 备注
         memo = request.data.get('memo')
         # 类型
         type = request.data.get('type')
         # 内容
         content = request.data.get('content')

         #增加反馈日志
         if file_id is not None and title is not None and memo is not None:
             feedbacklog = FeedBackLog(file_id=file_id,title=title,memo=memo)
             feedbacklog.save()

             # 如果存在富文本,则先添加富文本
             if type is not None and content is not None:
                 if type == 0:
                     feedbacktexts = FeedBackTexts(feedbacklog_id=feedbacklog.id,content=content)
                     feedbacktexts.save()

             #获取用户上传的文件,保存到服务器,再添加到数据库
             files = request.files.getlist('file')
             #判断文件列表是否存在文件
             if len(files) > 0:
                 #判断上传路径是否存在，不存在则创建
                 if not os.path.exists(settings.MEDIA_ROOT):
                     os.makedirs(settings.MEDIA_ROOT)
                 #遍历用户上传的文件列表
                 upload_files = []
                 for file in files:
                     #获取文件反缀名
                     extension = os.path.splitext(file.name)[1]
                     #通过uuid重命名上传的文件
                     filename = '{}{}'.format(uuid.uuid4(),extension)
                     #构建文件路径
                     file_path = '{}/{}'.format(settings.MEDIA_ROOT,filename)
                     #将上传的文件路径存储到upload_files中
                     #注意这样要构建相对路径MEDIA_URL+filename,这里可以保存到数据库
                     upload_files.append('{}{}'.format(settings.MEDIA_URL,filename))
                     #保存文件
                     with open(file_path,'wb') as f:
                         for c in file.chunks():
                             f.write(c)
                         f.close()

                     #增加反馈文件
                     feedbacks_ = FeedBacks(feedbacklog_id=feedbacklog.id,name=filename,path=file_path)
                     feedbacks_.save()

        except Exception as e:
           return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')

        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

class FileDownloadView(views.APIView):
    # 下载文件
    def get(self, request):
        filename = request.data.get('filename')
        filepath_ = os.path.abspath(os.path.join(os.getcwd(), 'uploadfiles')) + '/' + 'qrcode_for_gh_0ac60a1b8cd2_258.jpg'
        if os.path.isfile(filepath_):
            pass

        # 下载文件
        def readFile(fn, buf_size=262144):  # 大文件下载，设定缓存大小
            f = open(fn, "rb")
            while True:  # 循环读取
                c = f.read(buf_size)
                if c:
                    yield c
                else:
                    break
            f.close()

        from django.utils.http import urlquote

        file = open(filepath_, 'rb')
        response = FileResponse(file)
        response['content_type'] = 'APPLICATION/OCTET-STREAM'
        response['Content-Disposition'] = 'attachment; filename=' + urlquote(filename)  # 设定传输给客户端的文件名称
        response['Content-Length'] = os.path.getsize(filepath_)  # 传输给客户端的文件大小
        return response
