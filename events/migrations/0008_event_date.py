# Generated by Django 3.0.1 on 2019-12-24 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_event_contact_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(default='2017-04-12'),
            preserve_default=False,
        ),
    ]