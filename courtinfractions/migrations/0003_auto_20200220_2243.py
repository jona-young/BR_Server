# Generated by Django 3.0.2 on 2020-02-20 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courtinfractions', '0002_auto_20200220_2217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courtinf',
            old_name='date_posted',
            new_name='date',
        ),
    ]
