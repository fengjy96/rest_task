# Generated by Django 2.1.7 on 2019-07-03 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0022_auto_20190702_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steplog',
            name='memo',
            field=models.CharField(default='', max_length=300, verbose_name='备注'),
        ),
    ]
