# Generated by Django 3.0.1 on 2019-12-24 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20191224_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='facebook',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='website',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
