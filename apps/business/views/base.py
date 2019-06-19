from django.contrib.auth import get_user_model

from business.models.message import Message
from business.models.project import Project
from business.models.task import Task
from business.models.step import Step
from rbac.models import UserProfile
from business.models.message import Menu
from business.models.reason import Reason
from configuration.models.project_conf import ProjectStatus
from configuration.models.task_conf import TaskStatus
from configuration.models.reason_conf import ReasonType
from business.models.steplog import TaskLog
from business.models.files import Files, ProgressTexts
from django.db.models import Sum
import datetime

User = get_user_model()


class BusinessPublic:
    @classmethod
    def create_message(cls, sender_id, receiver_id, menu_id=1, messages=''):
        """
        创建消息
        :param sender_id:
        :param receiver_id:
        :param messages:
        :return:
        """
        sender = UserProfile.objects.get(id=sender_id)
        receiver = UserProfile.objects.get(id=receiver_id)
        menu = Menu.objects.get(id=menu_id)

        message = Message(
            title='提示',
            content=messages,
            sender=sender,
            receiver=receiver,
            status=0,
            menu=menu,
        )

        message.save()

    @classmethod
    def create_reason(cls, id, sender_id, receiver_id, reason_type_id, reason=''):
        """
        创建原因
        :param id:
        :param sender_id:
        :param receiver_id:
        :param key:
        :param reason:
        :return:
        """

        sender = UserProfile.objects.get(id=sender_id)
        receiver = UserProfile.objects.get(id=receiver_id)
        reason_type = ReasonType.objects.get(id=reason_type_id)

        reasons = Reason.objects.filter(type_id=reason_type.id, link_id=id)
        transfer_nums = reasons.count() + 1
        reason = Reason(
            type=reason_type,
            link_id=id,
            reason=reason,
            transfer_nums=transfer_nums,
            sender=sender,
            receiver=receiver
        )
        reason.save()

    @classmethod
    def Caltime(cls, date1, date2):
        """
        计算两个日期的时间差
        """
        return (date1 - date2).days + 1

    @classmethod
    def GetProjectStatusIdByKey(cls, key):
        """
        根据key值取项目状态表id值
        """
        return ProjectStatus.objects.get(key=key).id

    @classmethod
    def GetProjectStatusObjectByKey(cls, key):
        """
        根据key值取项目状态表对像
        """
        return ProjectStatus.objects.get(key=key)

    @classmethod
    def GetTaskStatusIdByKey(cls, key):
        """
        根据key值取任务状态表id值
        """
        return TaskStatus.objects.get(key=key).id

    @classmethod
    def GetTaskStatusObjectByKey(cls, key):
        """
        根据key值取任务状态表对像
        """
        return TaskStatus.objects.get(key=key)

    @classmethod
    def GetReasonTypeIdByKey(cls, key):
        """
        根据key值取原因类型表id值
        """
        return ReasonType.objects.get(key=key).id

    @classmethod
    def update_progress_by_project_id(cls, project_id):
        progress = 0
        tasks = Task.objects.filter(project_id=project_id, is_active=1)
        task_nums = tasks.count()
        checked_tasks = tasks.filter(receive_status_id=cls.GetTaskStatusIdByKey('checked')).aggregate(nums=Sum('progress'))
        if checked_tasks['nums'] is not None:
            progress = checked_tasks['nums']

        project_progress = progress / (task_nums * 100)
        project_progress = round(project_progress, 2)
        project_progress = int(project_progress * 100)

        project = Project.objects.get(id=project_id)
        if project:
            project.progress = project_progress
            if project_progress == 100:
                project.receive_status = cls.GetProjectStatusObjectByKey('finished')
                project.finish_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            project.save()

    @classmethod
    def update_progress_by_task_id(cls, task_id):
        progress = 0
        steps = Step.objects.filter(task_id=task_id, is_active=1)
        step_nums = steps.count()

        check_steps = Step.objects.filter(task_id=task_id, is_active=1).aggregate(nums=Sum('progress'))
        if check_steps['nums'] is not None:
            progress = check_steps['nums']

        task_progress = progress / (step_nums * 100)
        task_progress = round(task_progress, 2)
        task_progress = int(task_progress * 100)

        task = Task.objects.get(id=task_id)
        if task:
            task.progress = task_progress
            if task_progress == 100:
                task.receive_status = cls.GetTaskStatusObjectByKey('finished')
                task.finish_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            task.save()
            project_id = task.project_id
            cls.update_progress_by_project_id(project_id)

    @classmethod
    def create_task_file_texts(cls, task_id, files, content):
        # 增加日志
        if task_id is not None:
            if files or content:
                task_log = TaskLog(task_id=task_id)
                task_log.save()

                if files:
                    for file in files:
                        # 增加文件表记录
                        step_log_file = Files(tasklog=task_log, name=file['name'], path=file['url'],
                                              path_thumb_w200=file['path_thumb_w200'], path_thumb_w900=file['path_thumb_w900'])
                        step_log_file.save()

                # 如果存在富文本，则先添加富文本
                if content:
                    progresstexts = ProgressTexts(tasklog=task_log, content=content)
                    progresstexts.save()