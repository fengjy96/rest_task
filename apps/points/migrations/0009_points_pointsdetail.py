# Generated by Django 2.1.7 on 2019-06-04 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('points', '0008_auto_20190604_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_points', models.IntegerField(verbose_name='总积分')),
                ('available_points', models.IntegerField(verbose_name='可用积分')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户标识')),
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
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户标识')),
            ],
            options={
                'verbose_name': '用户积分明细',
                'verbose_name_plural': '用户积分明细',
            },
        ),
    ]
