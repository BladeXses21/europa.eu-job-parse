# Generated by Django 5.1.6 on 2025-04-21 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parser_app', '0011_jobdata_employer_legal_id_jobdata_eures_flag_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobdata',
            name='json_data',
        ),
    ]
