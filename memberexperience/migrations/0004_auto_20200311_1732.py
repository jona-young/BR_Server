# Generated by Django 3.0.2 on 2020-03-11 17:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('memberexperience', '0003_auto_20200311_1702'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memberrecord',
            old_name='Notes',
            new_name='notes',
        ),
        migrations.AddField(
            model_name='memberrecord',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='memberrecord',
            name='followUp1',
            field=models.DateField(default=datetime.datetime(2020, 6, 10, 17, 32, 37, 110505, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='memberrecord',
            name='followUp2',
            field=models.DateField(default=datetime.datetime(2020, 9, 9, 17, 32, 37, 110529, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='memberrecord',
            name='followUp3',
            field=models.DateField(default=datetime.datetime(2021, 3, 11, 17, 32, 37, 110540, tzinfo=utc)),
        ),
    ]
