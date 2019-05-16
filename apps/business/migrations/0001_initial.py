# Generated by Django 2.1.7 on 2019-05-16 17:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeedBackLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linkid', models.IntegerField(default=0, verbose_name='关链标识')),
                ('title', models.CharField(default='', max_length=150, verbose_name='标题')),
                ('memo', models.CharField(default='', max_length=300, verbose_name='备注')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否激活')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '反馈日志',
                'verbose_name_plural': '反馈日志',
            },
        ),
        migrations.CreateModel(
            name='FeedBacks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=150, verbose_name='文件名称')),
                ('path', models.CharField(default='', max_length=300, verbose_name='文件路径')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否激活')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '反馈',
                'verbose_name_plural': '反馈',
            },
        ),
        migrations.CreateModel(
            name='FeedBackTexts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(default=0, verbose_name='类型')),
                ('content', models.TextField(default='', max_length=80, verbose_name='内容')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否激活')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '反馈富文本',
            },
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=150, verbose_name='文件名称')),
                ('path', models.CharField(default='', max_length=300, verbose_name='文件路径')),
                ('type', models.IntegerField(default=1, verbose_name='类型')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否激活')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '文件',
                'verbose_name_plural': '文件',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=80, verbose_name='类型')),
                ('title', models.CharField(max_length=80, verbose_name='标题')),
                ('content', models.CharField(max_length=80, verbose_name='内容')),
                ('status', models.IntegerField(verbose_name='状态')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '消息',
                'verbose_name_plural': '消息',
            },
        ),
        migrations.CreateModel(
            name='ProgressTexts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(default=0, verbose_name='类型')),
                ('content', models.TextField(default='', max_length=80, verbose_name='内容')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否激活')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '富文本',
                'verbose_name_plural': '富文本',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=80, verbose_name='项目名')),
                ('style', models.CharField(default='', max_length=80, verbose_name='项目风格')),
                ('progress', models.IntegerField(default=0, verbose_name='项目进度')),
                ('points', models.IntegerField(default=0, verbose_name='项目积分')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否激活')),
                ('is_finished', models.IntegerField(default=0, verbose_name='是否完成')),
                ('customer', models.CharField(default='', max_length=80, verbose_name='客户')),
                ('receive_status', models.IntegerField(default=0, verbose_name='接收状态')),
                ('audit_status', models.IntegerField(default=0, verbose_name='审核状态')),
                ('begin_time', models.DateField(blank=True, null=True, verbose_name='项目开始时间')),
                ('end_time', models.DateField(blank=True, null=True, verbose_name='项目结束时间')),
                ('duration', models.FloatField(default=0, verbose_name='项目时长')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(blank=True, null=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
            },
        ),
        migrations.CreateModel(
            name='ProjectCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField(verbose_name='项目标识')),
                ('task_id', models.IntegerField(verbose_name='任务标识')),
                ('person_nums', models.IntegerField(verbose_name='人数')),
                ('duration', models.IntegerField(verbose_name=' 时限')),
                ('name', models.CharField(max_length=80, verbose_name='费用名称')),
                ('fee', models.FloatField(verbose_name='费用')),
                ('total_fee', models.FloatField(verbose_name='总费用')),
            ],
            options={
                'verbose_name': '项目成本',
                'verbose_name_plural': '项目成本',
            },
        ),
        migrations.CreateModel(
            name='ProjectFee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='费用名称')),
                ('value', models.FloatField(verbose_name='费用')),
            ],
            options={
                'verbose_name': '费用项',
                'verbose_name_plural': '费用项',
            },
        ),
        migrations.CreateModel(
            name='ProjectRejectReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(default='', max_length=80, verbose_name='项目驳回原因')),
                ('transfer_nums', models.IntegerField(default=0, verbose_name='驳回次数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '项目驳回原因',
                'verbose_name_plural': '项目驳回原因',
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=80, verbose_name='步骤名称')),
                ('index', models.IntegerField(blank=True, null=True, verbose_name='步骤序号')),
                ('progress', models.IntegerField(default=0, verbose_name='步骤进度')),
                ('is_active', models.IntegerField(default=0, verbose_name='是否激活')),
                ('is_finished', models.IntegerField(default=0, verbose_name='是否完成')),
                ('send_status', models.IntegerField(default=0, verbose_name='发送状态')),
                ('receive_status', models.IntegerField(default=0, verbose_name='接收状态')),
                ('audit_status', models.IntegerField(default=0, verbose_name='审核状态')),
                ('begin_time', models.DateTimeField(blank=True, null=True, verbose_name='步骤开始时间')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='步骤结束时间')),
                ('duration', models.FloatField(default=0, verbose_name='步骤时长')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(blank=True, null=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
            ],
            options={
                'verbose_name': '任务',
                'verbose_name_plural': '任务',
            },
        ),
        migrations.CreateModel(
            name='StepLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=150, verbose_name='标题')),
                ('progress', models.IntegerField(default=0, verbose_name='进度')),
                ('memo', models.CharField(default='', max_length=300, verbose_name='备注')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否激活')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '步骤日志',
                'verbose_name_plural': '步骤日志',
            },
        ),
        migrations.CreateModel(
            name='StepRejectReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(default='', max_length=100, verbose_name='驳回原因')),
                ('transfer_nums', models.IntegerField(default=0, verbose_name='驳回次数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '步骤驳回原因',
                'verbose_name_plural': '步骤驳回原因',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=80, verbose_name='任务名称')),
                ('content', models.TextField(default='', verbose_name='任务内容')),
                ('progress', models.IntegerField(default=0, verbose_name='任务进度')),
                ('begin_time', models.DateField(blank=True, null=True, verbose_name='开始时间')),
                ('end_time', models.DateField(blank=True, null=True, verbose_name='结束时间')),
                ('duration', models.FloatField(default=0, verbose_name='任务时长')),
                ('comments', models.CharField(blank=True, default='', max_length=80, null=True, verbose_name='任务评语')),
                ('points', models.IntegerField(default=0, verbose_name='任务积分')),
                ('memo', models.CharField(default='', max_length=800, verbose_name='任务备注')),
                ('send_status', models.IntegerField(default=0, verbose_name='发送状态')),
                ('receive_status', models.IntegerField(default=0, verbose_name='接收状态')),
                ('audit_status', models.IntegerField(default=0, verbose_name='审核状态')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否激活')),
                ('is_finished', models.IntegerField(default=0, verbose_name='是否完成')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(blank=True, null=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
            ],
            options={
                'verbose_name': '项目任务',
                'verbose_name_plural': '项目任务',
            },
        ),
        migrations.CreateModel(
            name='TaskAllocateReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(default='', max_length=100, verbose_name='转派原因')),
                ('transfer_nums', models.IntegerField(default=0, verbose_name='流转次数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '任务转派原因',
                'verbose_name_plural': '任务转派原因',
            },
        ),
    ]
