# Generated by Django 3.2.4 on 2021-06-13 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('short_video', '0007_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='onwer',
            new_name='owner',
        ),
    ]
