# Generated by Django 3.0.4 on 2020-03-28 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0010_auto_20200324_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='not_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 28, 15, 39, 7, 671067), verbose_name='date published'),
        ),
    ]
