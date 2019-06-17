from business.models.task import Task
from configuration.models.task_conf import TaskType, TaskQuality, TaskPriority, TaskStatus
from rbac.models import UserProfile
from business.models.project import Project
from business.views.base import BusinessPublic
# excel 读工具
import xlrd
from datetime import date


class Excel:
    @classmethod
    def import_excel_data(cls, project_id, file_name):
        obj = {}
        DataList = []
        try:
            with xlrd.open_workbook(file_name) as data:
                table = data.sheet_by_index(0)  # 获取工作表
                project_receiver_id = 0
                n = 1
                x = y = z = 0
                WorkList = []
                # nrows = table.nrows # 行数 ncols = table.ncols # 列数 print sh.row_values(rownum)
                for line in range(n, table.nrows):
                    n = n + 1
                    row = table.row_values(line)
                    # 查看行值是否为空
                    if row:
                        # 判断该行值是否在数据库中重复
                        if Task.objects.filter(name=row[0], project_id=project_id).exists():
                            x = x + 1  # 重复值计数
                            dict_obj = {}
                            dict_obj["info"] = '第' + str(n) + '行任务名称重复'
                            DataList.append(dict_obj)
                            z = z + 1
                            continue
                        else:
                            if not TaskType.objects.filter(name=row[1]).exists():
                                dict_obj = {}
                                dict_obj["info"] = '第' + str(n) + '行,第2列任务类型不存在'
                                DataList.append(dict_obj)
                                z = z + 1
                                continue
                            if not TaskPriority.objects.filter(name=row[3]).exists():
                                dict_obj = {}
                                dict_obj["info"] = '第' + str(n) + '行,第4列任务优先级不存在'
                                DataList.append(dict_obj)
                                z = z + 1
                                continue
                            if not TaskQuality.objects.filter(name=row[4]).exists():
                                dict_obj = {}
                                dict_obj["info"] = '第' + str(n) + '行,第5列任务品质要求不存在'
                                DataList.append(dict_obj)
                                z = z + 1
                                continue
                            if not UserProfile.objects.filter(name=row[7]).exists() and row[7] != '':
                                dict_obj = {}
                                dict_obj["info"] = '第' + str(n) + '行,第8列任务负责人不存在'
                                DataList.append(dict_obj)
                                z = z + 1
                                continue
                            if not cls.isVaildDate(row[5], data):
                                dict_obj = {}
                                dict_obj["info"] = '第' + str(n) + '行,第6列时间格式不正确'
                                DataList.append(dict_obj)
                                z = z + 1
                                continue
                            if not cls.isVaildDate(row[6], data):
                                dict_obj = {}
                                dict_obj["info"] = '第' + str(n) + '行,第7列时间格式不正确'
                                DataList.append(dict_obj)
                                z = z + 1
                                continue
                            if project_id is not None:
                                # 根据项目 id 查项目负责人
                                project = Project.objects.get(id=project_id)
                                project_receiver_id = project.receiver_id

                                # 如果项目状态为已完成，则当创建任务时，需要将项目状态改为已接手
                                if project.receive_status.key == 'finished':
                                    project.receive_status_id = BusinessPublic.GetProjectStatusIdByKey('accepted')
                                    project.save()

                            # 如果创建任务时指定了任务负责人，则任务接收状态为 1 - 已安排任务负责人
                            auditor = None
                            if row[7]:
                                if project_id is not None:
                                    # 根据项目 id 查项目审核状态
                                    project = Project.objects.get(id=project_id)
                                    if project.audit_status == 2:
                                        receive_status = BusinessPublic.GetTaskStatusObjectByKey('wait_accept')
                                    else:
                                        receive_status = BusinessPublic.GetTaskStatusObjectByKey('assigned')
                                else:
                                    receive_status = BusinessPublic.GetTaskStatusObjectByKey('assigned')
                            # 如果创建任务时未指定任务负责人，则任务接收状态为 0 - 未安排任务负责人
                            else:
                                receive_status = BusinessPublic.GetTaskStatusObjectByKey('unassigned')

                            # 如果存在项目负责人则将该项目负责人作为任务审核员
                            if project_receiver_id is not None:
                                auditor = UserProfile.objects.get(id=project_receiver_id)

                            project = Project.objects.get(id=project_id)
                            task_type = TaskType.objects.get(name=row[1])
                            task_priority = TaskPriority.objects.get(name=row[3])
                            task_quality = TaskQuality.objects.get(name=row[4])
                            receiver = UserProfile.objects.get(name=row[7])
                            sender = UserProfile.objects.get(id=project_receiver_id)

                            WorkList.append(Task(project=project,
                                                 name=row[0],
                                                 task_type=task_type,
                                                 content=row[2],
                                                 task_priority=task_priority,
                                                 task_quality=task_quality,
                                                 begin_time=cls.getDate(row[5], data),
                                                 end_time=cls.getDate(row[6], data),
                                                 receiver=receiver,
                                                 memo=row[8],
                                                 sender=sender,
                                                 auditor=auditor,
                                                 receive_status=receive_status,
                                                 ))

                            y = y + 1  # 非重复计数
                    else:
                        # 空行
                        z = z + 1
                        dict_obj = {}
                        dict_obj["info"] = '第' + str(n) + '行为空行'
                        DataList.append(dict_obj)

                    if (n - 1) % 2 == 0:
                        Task.objects.bulk_create(WorkList)
                        WorkList = []

                if len(WorkList) > 0:
                    Task.objects.bulk_create(WorkList)

                obj["success"] = y
                obj["fail"] = z
                obj['infos'] = DataList

        except Exception as e:
            dict_obj = {}
            dict_obj["info"] = '数据异常'
            DataList.append(dict_obj)
            obj['infos'] = DataList
            obj["success"] = 0
            return obj
        return obj

    @classmethod
    def isVaildDate(cls, value, data):
        try:
            value = xlrd.xldate_as_tuple(value, data.datemode)
            date(*value[:3]).strftime('%Y-%m-%d')
            return True
        except:
            return False

    @classmethod
    def getDate(cls, value, data):
        value = xlrd.xldate_as_tuple(value, data.datemode)
        return date(*value[:3]).strftime('%Y-%m-%d')