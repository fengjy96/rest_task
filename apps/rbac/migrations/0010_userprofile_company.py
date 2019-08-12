# Generated by Django 2.1.7 on 2019-07-18 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0009_remove_userprofile_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company', to='rbac.Organization', verbose_name='所属公司'),
        ),
    ]
