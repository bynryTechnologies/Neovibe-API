# Generated by Django 3.0.10 on 2021-03-10 16:31

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenant', '__first__'),
        ('utility', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='SopAssign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('asset_id', models.BigIntegerField(blank=True, null=True)),
                ('sop_master_detail', models.BigIntegerField(blank=True, null=True)),
                ('frequency_id', models.BigIntegerField(blank=True, null=True)),
                ('city_id', models.BigIntegerField(blank=True, null=True)),
                ('area_id', models.BigIntegerField(blank=True, null=True)),
                ('subarea_id', models.BigIntegerField(blank=True, null=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='ResourceAssign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('asset_id', models.BigIntegerField(blank=True, null=True)),
                ('user_id', models.BigIntegerField(blank=True, null=True)),
                ('city_id', models.BigIntegerField(blank=True, null=True)),
                ('area_id', models.BigIntegerField(blank=True, null=True)),
                ('subarea_id', models.BigIntegerField(blank=True, null=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='AsssetInsurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('asset_id', models.BigIntegerField(blank=True, null=True)),
                ('insurance_no', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('provider', models.CharField(blank=True, max_length=200, null=True)),
                ('cost', models.CharField(blank=True, max_length=200, null=True)),
                ('effective_start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('effective_end_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='AssetSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('category_id', models.BigIntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='AssetStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='AssetServiceHistoryStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='AssetServiceHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('asset_id', models.BigIntegerField(blank=True, null=True)),
                ('service_request', models.BigIntegerField(blank=True, null=True)),
                ('service_type', models.BigIntegerField(blank=True, null=True)),
                ('status_id', models.BigIntegerField(blank=True, null=True)),
                ('maintenance_cost', models.FloatField(default=Decimal('0'), max_length=200)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='AssetCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='AssetAmcContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('asset_id', models.BigIntegerField(blank=True, null=True)),
                ('contract_no', models.CharField(blank=True, max_length=200, null=True)),
                ('contract_name', models.CharField(blank=True, max_length=200, null=True)),
                ('contract_provider', models.CharField(blank=True, max_length=200, null=True)),
                ('cost', models.CharField(blank=True, max_length=200, null=True)),
                ('no_of_services', models.BigIntegerField(blank=True, null=True)),
                ('frequency', models.BigIntegerField(blank=True, null=True)),
                ('sop', models.BigIntegerField(blank=True, null=True)),
                ('effective_start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('effective_end_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('asset_no', models.CharField(blank=True, max_length=500, null=True, unique=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('serial_no', models.BigIntegerField(blank=True, null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=200, null=True)),
                ('make', models.CharField(blank=True, max_length=200, null=True)),
                ('model', models.CharField(blank=True, max_length=200, null=True)),
                ('category_id', models.BigIntegerField(blank=True, null=True)),
                ('sub_category_id', models.BigIntegerField(blank=True, null=True)),
                ('city_id', models.BigIntegerField(blank=True, null=True)),
                ('area_id', models.BigIntegerField(blank=True, null=True)),
                ('sub_area_id', models.BigIntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('lat', models.CharField(blank=True, max_length=200, null=True)),
                ('long', models.CharField(blank=True, max_length=200, null=True)),
                ('manufacturing_date', models.DateTimeField(blank=True, null=True)),
                ('installation_date', models.DateTimeField(blank=True, null=True)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
                ('asset_life', models.CharField(blank=True, max_length=200, null=True)),
                ('asset_value', models.BigIntegerField(blank=True, null=True)),
                ('deprecation_method', models.BigIntegerField(blank=True, null=True)),
                ('deprecation_rate', models.BigIntegerField(blank=True, null=True)),
                ('status_id', models.BigIntegerField(blank=True, null=True)),
                ('flag', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
    ]
