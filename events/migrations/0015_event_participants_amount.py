# Generated by Django 3.0.1 on 2020-01-05 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20200105_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='participants_amount',
            field=models.IntegerField(default=0),
        ),
    ]
