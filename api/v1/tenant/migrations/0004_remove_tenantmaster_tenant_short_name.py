# Generated by Django 3.0.11 on 2021-05-27 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0003_tenantmaster_tenant_short_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenantmaster',
            name='tenant_short_name',
        ),
    ]
