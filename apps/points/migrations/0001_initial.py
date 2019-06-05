# Generated by Django 2.1.7 on 2019-05-24 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_points', models.IntegerField(verbose_name='总积分')),
                ('available_points', models.IntegerField(verbose_name='可用积分')),
            ],
            options={
                'verbose_name': '用户积分',
                'verbose_name_plural': '用户积分',
            },
        ),
        migrations.CreateModel(
            name='PointsDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_points', models.IntegerField(verbose_name='本次操作的积分')),
                ('available_points', models.IntegerField(verbose_name='可用积分')),
                ('operation_type', models.IntegerField(verbose_name='操作类型')),
                ('points_type', models.IntegerField(verbose_name='积分类型')),
                ('points_status', models.IntegerField(verbose_name='积分状态')),
                ('points_source', models.IntegerField(verbose_name='积分来源')),
            ],
            options={
                'verbose_name': '用户积分明细',
                'verbose_name_plural': '用户积分明细',
            },
        ),
        migrations.CreateModel(
            name='ProjectPoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(verbose_name='积分')),
                ('link_id', models.IntegerField(verbose_name='项目或者任务标识')),
                ('type_id', models.IntegerField(verbose_name='积分类型')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否激活')),
            ],
            options={
                'verbose_name': '项目积分',
                'verbose_name_plural': '项目积分',
            },
        ),
    ]
