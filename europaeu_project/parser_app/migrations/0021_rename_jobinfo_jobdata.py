# Generated by Django 5.1.6 on 2025-04-22 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parser_app', '0020_jobinfo_delete_jobdata'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='JobInfo',
            new_name='JobData',
        ),
    ]
