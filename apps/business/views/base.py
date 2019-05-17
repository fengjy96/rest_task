from business.models.message import Message
from business.models.project import Project,ProjectRejectReason
from business.models.task import Task, TaskAllocateReason
from business.models.step import Step, StepRejectReason
from business.models.files import Files
import datetime
import time

class BusinessPublic:

    # 插入文件记录
    def create_filelist(self, company_id, file_name, file_type, file_desc, file_url, file_folder, file_size = 0, oldprogress = 0, newprogress = 0, task_id = 0, step_id = 0):
        #默认状态为激活
        is_active = 1

        files = Files(
            company_id=company_id,
            file_name=file_name,
            file_type=file_type,
            file_desc=file_desc,
            file_url=file_url,
            file_folder=file_folder,
            file_size=file_size,
            oldprogress=oldprogress,
            newprogress=newprogress,
            task_id=task_id,
            step_id=step_id,
            is_active=is_active
        )

        files.save()

    # 插入消息记录
    def create_message(self, sender_id, receiver_id, messages=''):

        title = '提示'
        status = 0

        message = Message(
            title=title,
            content=messages,
            sender_id=sender_id,
            receiver_id=receiver_id,
            status=status,
            menu_path='',
        )

        message.save()


    def create_resson(self, id, sender_id, receiver_id, tables='', reason=''):
        if tables == 'StepRejectReason':
            reasons = StepRejectReason.objects.filter(step_id=id)
            transfer_nums = reasons.count() + 1
            step_reject_reason = StepRejectReason(
                step_id=id,
                reason=reason,
                transfer_nums=transfer_nums,
                sender_id=sender_id,
                receiver_id=receiver_id
            )
            step_reject_reason.save()

        elif tables == 'TaskAllocateReason':
            reasons = TaskAllocateReason.objects.filter(task_id=id)
            transfer_nums = reasons.count() + 1

            task_allocate_reason = TaskAllocateReason(
                task_id=id,
                reason=reason,
                transfer_nums=transfer_nums,
                receiver_id=receiver_id,
                sender=sender_id,
                receiver=receiver_id,
            )

            task_allocate_reason.save()

        else:
            reasons = ProjectRejectReason.objects.filter(project_id=id)
            transfer_nums = reasons.count() + 1

            project_reject_reason = ProjectRejectReason(
                project_id=id,
                reason=reason,
                transfer_nums=transfer_nums,
                sender_id=sender_id,
                receiver_id=receiver_id
            )

            project_reject_reason.save()

    # 根据任务步骤百分比更新任务百分比
    def update_task_progress(self, step_id=0):
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

    # 根据任务百分比更新项目百分比
    def update_project_progress(self, step_id=0):
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

    #计算两个日期相差天数，自定义函数名，和两个日期的变量名。
    def Caltime(date1,date2):
        #%Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
        #date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
        #date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
        date1=time.strptime(date1,"%Y-%m-%d")
        date2=time.strptime(date2,"%Y-%m-%d")
        #根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
        #date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
        #date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
        date1=datetime.datetime(date1[0],date1[1],date1[2])
        date2=datetime.datetime(date2[0],date2[1],date2[2])
        #返回两个变量相差的值，就是相差天数
        return date2-date1