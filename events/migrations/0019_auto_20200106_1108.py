# Generated by Django 3.0.1 on 2020-01-06 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_auto_20200106_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_status',
            field=models.CharField(choices=[('Aktywne', 'Aktywne'), ('Zakończone', 'Zakończone'), ('Wstrzymane', 'Wstrzymane')], default='Aktywne', max_length=64, null=True),
        ),
    ]
