# Generated by Django 2.1.7 on 2019-06-06 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0010_progresstexts_tasklog'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='finish_time',
            field=models.DateTimeField(auto_now=True, verbose_name='完成时间'),
        ),
        migrations.AddField(
            model_name='step',
            name='finish_time',
            field=models.DateTimeField(auto_now=True, verbose_name='完成时间'),
        ),
        migrations.AddField(
            model_name='task',
            name='finish_time',
            field=models.DateTimeField(auto_now=True, verbose_name='完成时间'),
        ),
    ]
