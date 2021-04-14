# Generated by Django 3.0.3 on 2021-04-10 10:04

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0005_utilitymaster_user_id'),
        ('tenant', '0001_initial'),
        ('billing', '0011_auto_20210406_0837'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('template_sections_json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('rendering_template', models.CharField(blank=True, max_length=200, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.DeleteModel(
            name='BillInvoiceSection',
        ),
        migrations.RemoveField(
            model_name='renderinvoicetemplate',
            name='tenant',
        ),
        migrations.RemoveField(
            model_name='renderinvoicetemplate',
            name='utility',
        ),
        migrations.DeleteModel(
            name='BillInvoiceSectionMaster',
        ),
        migrations.DeleteModel(
            name='RenderInvoiceTemplate',
        ),
    ]