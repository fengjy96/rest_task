# Generated by Django 2.1.7 on 2019-05-28 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0002_userprofile_base_salary'),
        ('business', '0005_auto_20190528_1032'),
        ('points', '0003_merge_20190528_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpoints',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_points_project_id', to='business.Project', verbose_name='项目标识'),
        ),
        migrations.AddField(
            model_name='projectpoints',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_points_task_id', to='rbac.Role', verbose_name='任务标识'),
        ),
        migrations.AddField(
            model_name='projectpoints',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_points_task_id', to='business.Task', verbose_name='任务标识'),
        ),
        migrations.AlterField(
            model_name='projectpoints',
            name='points',
            field=models.IntegerField(default=0, verbose_name='积分'),
        ),
        migrations.AlterField(
            model_name='projectpoints',
            name='type_id',
            field=models.IntegerField(default=0, verbose_name='积分类型'),
        ),
        migrations.AlterField(
            model_name='projectpoints',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_points_user_id', to=settings.AUTH_USER_MODEL, verbose_name='用户标识'),
        ),
    ]
