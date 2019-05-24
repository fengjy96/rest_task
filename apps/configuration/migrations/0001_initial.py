# Generated by Django 2.1.7 on 2019-05-24 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(verbose_name='排序')),
                ('value', models.IntegerField(verbose_name='状态真实序号')),
                ('key', models.CharField(max_length=30, verbose_name='状态英文表示')),
                ('text', models.CharField(max_length=30, verbose_name='状态中文表示')),
                ('desc', models.CharField(blank=True, max_length=50, null=True, verbose_name='状态描述')),
            ],
            options={
                'verbose_name': '项目状态',
                'verbose_name_plural': '项目状态',
            },
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wage', models.FloatField(verbose_name='工资')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否激活')),
            ],
            options={
                'verbose_name': '薪水',
                'verbose_name_plural': '薪水',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否激活')),
            ],
            options={
                'verbose_name': '用户技能',
                'verbose_name_plural': '用户技能',
            },
        ),
        migrations.CreateModel(
            name='TaskAssessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='评级名称')),
                ('index', models.IntegerField(verbose_name='评级序号')),
                ('weight', models.FloatField(verbose_name='权重')),
                ('is_active', models.IntegerField(verbose_name='是否激活')),
            ],
            options={
                'verbose_name': '任务评级',
                'verbose_name_plural': '任务评级',
            },
        ),
        migrations.CreateModel(
            name='TaskDesignType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='设计方式名称')),
                ('index', models.IntegerField(verbose_name='设计方式序号')),
                ('is_active', models.IntegerField(verbose_name='是否激活')),
            ],
            options={
                'verbose_name': '任务设计方式',
                'verbose_name_plural': '任务设计方式',
            },
        ),
        migrations.CreateModel(
            name='TaskPriority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='优先级名称')),
                ('index', models.IntegerField(verbose_name='优先级序号')),
                ('weight', models.FloatField(verbose_name='权重')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否激活')),
            ],
            options={
                'verbose_name': '任务优先级',
                'verbose_name_plural': '任务优先级',
            },
        ),
        migrations.CreateModel(
            name='TaskQuality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='品质要求名称')),
                ('index', models.IntegerField(verbose_name='品质要求序号')),
                ('weight', models.FloatField(verbose_name='权重')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否激活')),
            ],
            options={
                'verbose_name': '任务品质要求',
                'verbose_name_plural': '任务品质要求',
            },
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(verbose_name='排序')),
                ('value', models.IntegerField(verbose_name='状态真实序号')),
                ('key', models.CharField(max_length=30, verbose_name='状态英文表示')),
                ('text', models.CharField(max_length=30, verbose_name='状态中文表示')),
                ('desc', models.CharField(blank=True, max_length=60, null=True, verbose_name='状态描述')),
            ],
            options={
                'verbose_name': '任务状态',
                'verbose_name_plural': '任务状态',
            },
        ),
        migrations.CreateModel(
            name='TaskStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='任务步骤名称')),
                ('index', models.IntegerField(verbose_name='步骤序号')),
                ('is_active', models.IntegerField(verbose_name='是否激活')),
            ],
            options={
                'verbose_name': '任务步骤',
                'verbose_name_plural': '任务步骤',
            },
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='类型名称')),
                ('index', models.IntegerField(verbose_name='类型序号')),
                ('is_active', models.IntegerField(verbose_name='是否激活')),
            ],
            options={
                'verbose_name': '任务类型',
                'verbose_name_plural': '任务类型',
            },
        ),
    ]
