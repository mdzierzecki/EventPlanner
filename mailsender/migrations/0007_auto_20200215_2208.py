# Generated by Django 3.0.3 on 2020-02-15 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailsender', '0006_mailing_emails_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='send_date',
            field=models.DateTimeField(blank=True, help_text='When mailing was send', null=True, verbose_name='Sent at'),
        ),
    ]
