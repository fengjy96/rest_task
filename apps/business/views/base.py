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
    def create_message(self, sender_id, receiver_id, menu_id=1, messages=''):
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
    def create_reason(self, id, sender_id, receiver_id, reason_type_id, reason=''):
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
    def Caltime(self, date1, date2):
        """
        计算两个日期的时间差
        """
        return (date1 - date2).days

    @classmethod
    def GetProjectStatusIdByKey(self, key):
        """
        根据key值取项目状态表id值
        """
        return ProjectStatus.objects.get(key=key).id

    @classmethod
    def GetProjectStatusObjectByKey(self, key):
        """
        根据key值取项目状态表对像
        """
        return ProjectStatus.objects.get(key=key)

    @classmethod
    def GetTaskStatusIdByKey(self, key):
        """
        根据key值取任务状态表id值
        """
        return TaskStatus.objects.get(key=key).id

    @classmethod
    def GetTaskStatusObjectByKey(self, key):
        """
        根据key值取任务状态表对像
        """
        return TaskStatus.objects.get(key=key)

    @classmethod
    def GetReasonTypeIdByKey(self, key):
        """
        根据key值取原因类型表id值
        """
        return ReasonType.objects.get(key=key).id

    @classmethod
    def update_task_progress(self, step_id=0):
        """
        根据任务步骤百分比更新任务百分比
        """
        if step_id is not None:
            # 任务百分比
            task_progress = 0
            step = Step.objects.get(id=step_id)
            if step is not None:
                task_id = step.task_id
                # 所有生效的任务步骤,包括未审核通过
                steps_all = Step.objects.filter(task_id=task_id, is_active=1)
                step_nums = steps_all.count()

                # 所有生效的审核通过的任务步骤
                steps_preview = Step.objects.filter(task_id=task_id, is_active=1, audit_status=2)
                for step in steps_preview:
                    progress = steps_preview.progress
                    step_percentage = progress / (step_nums * 100)
                    step_percentage = round(step_percentage, 2)
                    step_percentage = step_percentage * 100
                    task_progress = task_progress + step_percentage

                task = Task.objects.get(id=task_id)
                if task is not None:
                    task.progress = task_progress
                    task.save()

    @classmethod
    def update_project_progress(self, step_id=0):
        """
        根据任务百分比更新项目百分比
        """
        if step_id is not None:
            # 任务百分比
            project_progress = 0

            step = Step.objects.get(id=step_id)
            if step is not None:
                task_id = step.task_id
                task = Task.objects.get(id=task_id)
                if task is not None:
                    project_id = task.project_id

                    # 所有生效的任务
                    tasks_all = Task.objects.filter(project_id=task_id, is_active=1, audit_status=2)
                    tasks_nums = tasks_all.count()

                    for tasks in tasks_all:
                        progress = tasks_all.progress
                        task_percentage = progress / (tasks_nums * 100)
                        task_percentage = round(task_percentage, 2)
                        task_percentage = task_percentage * 100
                        project_progress = project_progress + task_percentage

                    project = Project.objects.get(id=project_id)
                    if project is not None:
                        project.progress = project_progress
                        project.save()
