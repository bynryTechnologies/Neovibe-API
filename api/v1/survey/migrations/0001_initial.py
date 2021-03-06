# Generated by Django 3.0.3 on 2021-04-19 07:27

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
            name='SurveyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyTransactionStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.CharField(max_length=200)),
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
            name='SurveySubType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('survey_type_id', models.BigIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyStatus',
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
            name='SurveyObjective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('objective', models.CharField(max_length=500)),
                ('survey_type_id', models.BigIntegerField(blank=True, null=True)),
                ('survey_subtype_id', models.BigIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyConsumer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('survey_id', models.BigIntegerField()),
                ('vendor_id', models.BigIntegerField()),
                ('consumer_no', models.CharField(max_length=200)),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('email_id', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_mobile', models.CharField(blank=True, max_length=200, null=True)),
                ('address_line_1', models.CharField(blank=True, max_length=500, null=True)),
                ('street', models.CharField(blank=True, max_length=200, null=True)),
                ('zipcode', models.BigIntegerField(blank=True, null=True)),
                ('area_id', models.BigIntegerField(blank=True, null=True)),
                ('sub_area_id', models.BigIntegerField(blank=True, null=True)),
                ('category_id', models.BigIntegerField(blank=True, null=True)),
                ('sub_category_id', models.BigIntegerField(blank=True, null=True)),
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
            name='SurveyAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('survey_id', models.BigIntegerField()),
                ('vendor_id', models.BigIntegerField()),
                ('assigned_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('completion_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('status_id', models.BigIntegerField(blank=True, null=True)),
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
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('objective_id', models.BigIntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('type_id', models.BigIntegerField(blank=True, null=True)),
                ('category_id', models.BigIntegerField(blank=True, null=True)),
                ('sub_category_id', models.BigIntegerField(blank=True, null=True)),
                ('no_of_consumers', models.BigIntegerField(blank=True, null=True)),
                ('start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('end_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('area_id', models.BigIntegerField(blank=True, null=True)),
                ('sub_area_id', models.BigIntegerField(blank=True, null=True)),
                ('status_id', models.BigIntegerField(blank=True, null=True)),
                ('completion_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
    ]
