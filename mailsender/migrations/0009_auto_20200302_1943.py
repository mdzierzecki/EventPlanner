# Generated by Django 3.0.3 on 2020-03-02 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailsender', '0008_mailing_zipevent_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='subject',
            field=models.CharField(max_length=50),
        ),
    ]