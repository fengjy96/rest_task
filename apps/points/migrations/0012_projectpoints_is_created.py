# Generated by Django 2.1.7 on 2019-06-11 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0011_auto_20190611_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpoints',
            name='is_created',
            field=models.IntegerField(default=0, verbose_name='是否已生成积分'),
        ),
    ]
