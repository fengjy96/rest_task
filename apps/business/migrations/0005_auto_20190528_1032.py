# Generated by Django 2.1.7 on 2019-05-28 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0005_auto_20190528_1032'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0004_merge_20190528_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_id', models.IntegerField(default=0, verbose_name='关链标识')),
                ('reason', models.CharField(default='', max_length=180, verbose_name='原因')),
                ('transfer_nums', models.IntegerField(default=0, verbose_name='次数')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reason_receiver_id', to=settings.AUTH_USER_MODEL, verbose_name='接收者')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reason_sender_id', to=settings.AUTH_USER_MODEL, verbose_name='发送者')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reason_type', to='configuration.ReasonType', verbose_name='原因类型')),
            ],
            options={
                'verbose_name': '原因',
                'verbose_name_plural': '原因',
            },
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=150, verbose_name='标题')),
                ('memo', models.CharField(default='', max_length=300, verbose_name='备注')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否激活')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '任务日志',
                'verbose_name_plural': '任务日志',
            },
        ),
        migrations.RenameField(
            model_name='feedbacklog',
            old_name='linkid',
            new_name='link_id',
        ),
        migrations.RemoveField(
            model_name='files',
            name='task',
        ),
        migrations.AddField(
            model_name='feedbacklog',
            name='type',
            field=models.IntegerField(default=1, verbose_name='类型'),
        ),
        migrations.AddField(
            model_name='feedbacks',
            name='type',
            field=models.IntegerField(default=1, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='feedbacktexts',
            name='content',
            field=models.TextField(default='', verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='files',
            name='steplog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.StepLog', verbose_name='步骤日志标识'),
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to=settings.AUTH_USER_MODEL, verbose_name='接收者'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to=settings.AUTH_USER_MODEL, verbose_name='发送者'),
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.IntegerField(default=1, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='message',
            name='title',
            field=models.CharField(blank=True, max_length=180, null=True, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='message',
            name='type',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='progresstexts',
            name='content',
            field=models.TextField(default='', verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='project',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to='rbac.Company', verbose_name='公司标识'),
        ),
        migrations.AlterField(
            model_name='projectcost',
            name='task_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_cost_task_type_id', to='configuration.TaskType', verbose_name='任务类型'),
        ),
        migrations.AlterField(
            model_name='projectcost',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_cost_user_id', to=settings.AUTH_USER_MODEL, verbose_name='用户标识'),
        ),
        migrations.AlterField(
            model_name='projectfee',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Company', verbose_name='公司标识'),
        ),
        migrations.AlterField(
            model_name='projectfee',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.Project', verbose_name='项目标识'),
        ),
        migrations.AlterField(
            model_name='projectrejectreason',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_reject_reason_project_id', to='business.Project', verbose_name='项目标识'),
        ),
        migrations.AlterField(
            model_name='projectrejectreason',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_reject_reason_receiver_id', to=settings.AUTH_USER_MODEL, verbose_name='接收者'),
        ),
        migrations.AlterField(
            model_name='projectrejectreason',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_reject_reason_sender_id', to=settings.AUTH_USER_MODEL, verbose_name='发送者'),
        ),
        migrations.AlterField(
            model_name='step',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.Task', verbose_name='任务标识'),
        ),
        migrations.AlterField(
            model_name='step',
            name='task_design_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configuration.TaskDesignType', verbose_name='设计方式'),
        ),
        migrations.AlterField(
            model_name='steplog',
            name='step',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.Step', verbose_name='步骤标识'),
        ),
        migrations.AlterField(
            model_name='steprejectreason',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='step_reject_reason_receiver', to=settings.AUTH_USER_MODEL, verbose_name='接收者'),
        ),
        migrations.AlterField(
            model_name='steprejectreason',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='step_reject_reason_sender', to=settings.AUTH_USER_MODEL, verbose_name='发送者'),
        ),
        migrations.AlterField(
            model_name='steprejectreason',
            name='step',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.Step', verbose_name='步骤标识'),
        ),
        migrations.AlterField(
            model_name='task',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.Project', verbose_name='项目标识'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_priority',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configuration.TaskPriority', verbose_name='任务优先级'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_quality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configuration.TaskQuality', verbose_name='任务质量'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configuration.TaskType', verbose_name='任务类型标识'),
        ),
        migrations.AddField(
            model_name='tasklog',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.Task', verbose_name='任务标识'),
        ),
        migrations.AddField(
            model_name='files',
            name='tasklog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.TaskLog', verbose_name='任务日志标识'),
        ),
    ]
