from django.contrib.auth import get_user_model

from business.models.message import Message
from business.models.project import Project
from business.models.task import Task
from business.models.step import Step
from rbac.models import UserProfile
from business.models.message import Menu
from business.models.reason import Reason
from configuration.models import ProjectStatus, TaskStatus, ReasonType

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
        return (date1 - date2).days

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
        tasks = Task.objects.filter(project_id=project_id, is_active=1)
        task_nums = tasks.count()
        checked_tasks = tasks.filter(receive_status_id=cls.GetTaskStatusIdByKey('checked'))

        project_progress = 0
        for task in checked_tasks:
            progress = task.progress
            task_percentage = progress / (task_nums * 100)
            task_percentage = round(task_percentage, 2)
            task_percentage = task_percentage * 100
            project_progress = int(project_progress + task_percentage)

        project = Project.objects.get(id=project_id)
        if project:
            project.progress = project_progress
            if project_progress == 100:
                project.receive_status = cls.GetProjectStatusObjectByKey('finished')
            project.save()

    @classmethod
    def update_progress_by_task_id(cls, task_id):
        steps = Step.objects.filter(task_id=task_id, is_active=1)
        step_nums = steps.count()

        task_progress = 0
        for step in steps:
            progress = step.progress
            step_percentage = progress / (step_nums * 100)
            step_percentage = round(step_percentage, 2)
            step_percentage = step_percentage * 100
            task_progress = int(task_progress + step_percentage)

        task = Task.objects.get(id=task_id)
        if task:
            task.progress = task_progress
            if task_progress == 100:
                task.receive_status = cls.GetTaskStatusObjectByKey('finished')
            task.save()
            project_id = task.project_id
            cls.update_progress_by_project_id(project_id)
