# Generated by Django 3.0.1 on 2020-01-06 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_event_event_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_status',
            field=models.CharField(choices=[('Aktywne', 'Aktywne'), ('Zakonczone', 'Zakonczone'), ('Wstrzymane', 'Wstrzymane')], default='Aktywne', max_length=64, null=True),
        ),
    ]
