# Generated by Django 2.2.7 on 2019-12-21 22:21

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20191218_1057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='surname',
        ),
        migrations.AddField(
            model_name='participant',
            name='email',
            field=models.EmailField(default='abb@ccc.pl', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='reg_date',
            field=models.DateTimeField(auto_now_add=True, help_text='When participant jointed event', verbose_name='Created at'),
        ),
    ]
