# Generated by Django 3.0.1 on 2019-12-24 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20191224_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='street',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
