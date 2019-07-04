import os
import uuid
import time

from PIL import Image
from rest_framework import views
from rest_framework.response import Response

from utils.basic import MykeyResponse
from rest_framework import status
from django.http import FileResponse
from django.conf import settings


class UploadFilesView(views.APIView):
    """
    上传单个或者多个文件
    """

    def post(self, request):
        try:
            # 获取用户上传的文件,保存到服务器,再添加到数据库
            files = request.FILES.getlist('file')
            # 判断文件列表是否存在文件
            if len(files) > 0:
                # 遍历用户上传的文件列表
                upload_files = []
                dict_obj = {}
                for file in files:
                    # 获取文件后缀名
                    extension = os.path.splitext(file.name)[1][1:]
                    # 根据文件类型生成相对应的文件夹-时间+类型
                    path_year = time.strftime('%Y', time.localtime())
                    path_month = time.strftime('%m', time.localtime())
                    path_day = time.strftime('%d', time.localtime())

                    path = '{}/{}/{}/{}/{}/{}'.format(settings.MEDIA_ROOT, 'project', path_year, path_month, path_day,
                                                      extension)
                    # 判断上传路径是否存在，不存在则创建
                    if not os.path.exists(path):
                        os.makedirs(path)

                    # 通过 uuid 重命名上传的文件
                    filename = '{}.{}'.format(uuid.uuid4(), extension)
                    # 构建文件路径
                    file_path = '{}{}/{}/{}/{}/{}/{}'.format(settings.MEDIA_URL, 'project', path_year, path_month,
                                                             path_day, extension, filename)
                    file_path_server = '{}/{}/{}/{}/{}/{}/{}'.format(settings.MEDIA_ROOT, 'project', path_year,
                                                                     path_month, path_day, extension, filename)

                    # 如果上传的文件是图片类型，则生成相应尺寸的缩略图
                    img_formats = ['jpg', 'jpeg', 'png', 'bmp', 'gif']
                    if extension in img_formats:
                        img = Image.open(file)
                        img_w900 = self.make_thumb(img, 900)
                        img_w900.save(file_path_server + '_w900.' + extension)
                        img_w200 = self.make_thumb(img, 200)
                        img_w200.save(file_path_server + '_w200.' + extension)
                        dict_obj["path_thumb_w200"] = file_path + '_w200.' + extension
                        dict_obj["path_thumb_w900"]  = file_path + '_w900.' + extension

                    # 将上传的文件路径存储到 upload_files 中
                    # 注意这样要构建相对路径 MEDIA_URL + filename，这里可以保存到数据库
                    dict_obj["name"] = filename
                    dict_obj["raw_name"] = file.name
                    dict_obj["url"] = file_path

                    upload_files.append(dict_obj)
                    # 保存文件
                    with open(file_path_server, 'wb') as f:
                        for c in file.chunks():
                            f.write(c)
                        f.close()

                data = {'files': upload_files}

                return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=data)

        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')

    def make_thumb(self, img, size=150):
        width, height = img.size
        if width > size:
            delta = width / size
            height = int(height / delta)
            img.thumbnail((width, height), Image.ANTIALIAS)
        return img


class UploadRteFilesView(views.APIView):
    """
    用于兼容 froala 富文本编辑器的文件上传
    """

    def post(self, request):
        try:
            # 获取用户上传的文件,保存到服务器,再添加到数据库
            files = request.FILES.getlist('file', [])
            # 判断文件列表是否存在文件
            if len(files) > 0:
                # 判断上传路径是否存在，不存在则创建
                if not os.path.exists(settings.MEDIA_ROOT):
                    os.makedirs(settings.MEDIA_ROOT)

                file = files[0]
                # 获取文件后缀名
                extension = os.path.splitext(file.name)[1]
                # 通过uuid重命名上传的文件
                filename = '{}{}'.format(uuid.uuid4(), extension)
                # 构建文件路径
                file_path = '{}{}'.format(settings.MEDIA_URL, filename)
                file_path_server = '{}/{}'.format(settings.MEDIA_ROOT, filename)

                # 保存文件
                with open(file_path_server, 'wb') as f:
                    for c in file.chunks():
                        f.write(c)
                    f.close()

                data = {'link': file_path}
                return Response(data=data)
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')


class DeleteFileView(views.APIView):
    """
    删除单个文件或者多个文件
    """

    def post(self, request):
        try:
            # 获取文件名称列表
            urls = request.POST.getlist('url')
            # 判断是否存在文件列表
            if len(urls) > 0:
                # 判断文件径是否存在，存在则删除
                for url in urls:
                    if os.path.exists(url):
                        os.remove(url)

                return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')


class FileDownloadView(views.APIView):
    # 下载文件
    def get(self, request):
        filename = request.data.get('filename')
        filepath_ = os.path.abspath(os.path.join(os.getcwd(), 'uploadfiles')) + '/' + filename
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
