# Generated by Django 3.0.1 on 2019-12-24 14:59

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_event_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='contact_description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]