# Generated by Django 2.1.7 on 2019-06-06 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0009_auto_20190530_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='finish_time',
            field=models.DateField(blank=True, null=True, verbose_name='项目完成时间'),
        ),
        migrations.AddField(
            model_name='step',
            name='finish_time',
            field=models.DateField(blank=True, null=True, verbose_name='完成时间'),
        ),
        migrations.AddField(
            model_name='task',
            name='finish_time',
            field=models.DateField(blank=True, null=True, verbose_name='完成时间'),
        ),
        migrations.AlterField(
            model_name='step',
            name='begin_time',
            field=models.DateField(blank=True, null=True, verbose_name='开始时间'),
        ),
        migrations.AlterField(
            model_name='step',
            name='end_time',
            field=models.DateField(blank=True, null=True, verbose_name='结束时间'),
        ),
    ]
