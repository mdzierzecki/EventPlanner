# Generated by Django 3.0.3 on 2020-02-14 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailsender', '0002_remove_mailing_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='status',
            field=models.CharField(choices=[('Gotowy do wysyłki', 'Gotowy do wysyłki'), ('Wysyłanie', 'Wysyłanie'), ('Wysłany', 'Wysłany'), ('Błąd', 'Błąd')], default='Gotowy do wysyłki', max_length=64, null=True),
        ),
    ]
