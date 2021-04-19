# Generated by Django 3.0.3 on 2021-04-19 07:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import fsm.fsm
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('tenant', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=200, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('masteruser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('user_id', models.CharField(blank=True, max_length=200, null=True)),
                ('city_id', models.BigIntegerField(blank=True, null=True)),
                ('user_type_id', models.BigIntegerField(blank=True, null=True)),
                ('user_subtype_id', models.BigIntegerField(blank=True, null=True)),
                ('form_factor_id', models.BigIntegerField(blank=True, null=True)),
                ('department_id', models.BigIntegerField(blank=True, null=True)),
                ('status_id', models.BigIntegerField(blank=True, null=True)),
                ('state', models.BigIntegerField(choices=[(0, 'CREATED'), (1, 'ACTIVE'), (2, 'INACTIVE'), (3, 'ARCHIVED')], default=0)),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('middle_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('user_image', models.URLField(blank=True, null=True)),
                ('phone_mobile', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_landline', models.CharField(blank=True, max_length=200, null=True)),
                ('supplier_id', models.BigIntegerField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('master.masteruser', models.Model, fsm.fsm.FiniteStateMachineMixin),
        ),
    ]
