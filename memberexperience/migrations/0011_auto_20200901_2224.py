# Generated by Django 3.1 on 2020-09-02 02:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('memberexperience', '0010_auto_20200830_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberrecord',
            name='followUp1',
            field=models.DateField(default=datetime.datetime(2020, 12, 2, 2, 24, 39, 104195, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='memberrecord',
            name='followUp2',
            field=models.DateField(default=datetime.datetime(2021, 3, 3, 2, 24, 39, 104231, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='memberrecord',
            name='followUp3',
            field=models.DateField(default=datetime.datetime(2021, 9, 2, 2, 24, 39, 104249, tzinfo=utc)),
        ),
    ]
