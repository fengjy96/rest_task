# Generated by Django 2.1.7 on 2019-06-19 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0003_auto_20190613_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='avatar/image/default.png', null=True, upload_to=''),
        ),
    ]