# Generated by Django 3.0.3 on 2020-02-23 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0027_delete_mailing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(max_length=70),
        ),
    ]
