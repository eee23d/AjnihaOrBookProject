# Generated by Django 3.2.3 on 2021-06-12 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AJNIHA', '0020_alter_readingrecords_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='bookLink',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
