# Generated by Django 3.0.3 on 2020-02-14 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0025_mailing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mailing',
            old_name='description',
            new_name='text',
        ),
    ]