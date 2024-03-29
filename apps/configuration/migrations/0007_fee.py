# Generated by Django 2.1.7 on 2019-06-03 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0006_merge_20190530_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='费用名称')),
                ('value', models.IntegerField(default=0, verbose_name='费用')),
            ],
            options={
                'verbose_name': '基本费用',
                'verbose_name_plural': '基本费用',
            },
        ),
    ]
