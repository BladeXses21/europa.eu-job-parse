# Generated by Django 5.1.6 on 2025-04-22 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parser_app', '0017_remove_jobdata_connection_point_id_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='JobData',
            new_name='JobInfo',
        ),
    ]
