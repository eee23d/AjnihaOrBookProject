# Generated by Django 3.2.3 on 2021-05-30 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AJNIHA', '0015_contacts_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readeraccount',
            name='prof_pic',
            field=models.ImageField(blank=True, default='/default.jpg', null=True, upload_to=''),
        ),
    ]
