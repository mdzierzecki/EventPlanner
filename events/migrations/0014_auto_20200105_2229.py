# Generated by Django 3.0.1 on 2020-01-05 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20191224_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_status',
            field=models.CharField(choices=[('Aktywne', 'Aktywne'), ('Zakończone', 'Zakończone'), ('Wstrzymane', 'Wstrzymane')], default='Aktywne', max_length=64, null=True),
        ),
    ]