# Generated by Django 2.1.7 on 2019-06-11 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0013_pointsdetail_add_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='total_coins',
            field=models.FloatField(default=0, verbose_name='米值'),
        ),
    ]
