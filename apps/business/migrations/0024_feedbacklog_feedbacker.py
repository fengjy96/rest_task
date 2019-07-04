# Generated by Django 2.1.7 on 2019-07-03 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0023_auto_20190703_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbacklog',
            name='feedbacker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacker', to=settings.AUTH_USER_MODEL, verbose_name='反馈者'),
        ),
    ]
