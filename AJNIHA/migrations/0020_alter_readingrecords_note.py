# Generated by Django 3.2.3 on 2021-06-11 03:52

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AJNIHA', '0019_auto_20210611_0637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readingrecords',
            name='note',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
