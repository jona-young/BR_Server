# Generated by Django 3.1 on 2020-09-03 03:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('memberexperience', '0005_auto_20200902_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberrecord',
            name='followUp1',
            field=models.DateField(default=datetime.datetime(2020, 12, 3, 3, 15, 52, 694336, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='memberrecord',
            name='followUp2',
            field=models.DateField(default=datetime.datetime(2021, 3, 4, 3, 15, 52, 694359, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='memberrecord',
            name='followUp3',
            field=models.DateField(default=datetime.datetime(2021, 9, 3, 3, 15, 52, 694370, tzinfo=utc)),
        ),
    ]