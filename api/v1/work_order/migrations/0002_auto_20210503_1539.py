# Generated by Django 3.0.3 on 2021-05-03 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceassignment',
            name='assignment_time',
        ),
        migrations.RemoveField(
            model_name='serviceassignment',
            name='completion_time',
        ),
    ]
