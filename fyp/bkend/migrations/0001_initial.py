# Generated by Django 5.1.7 on 2025-03-26 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('identity_card', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('primary_email', models.EmailField(max_length=254, unique=True)),
                ('secondary_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact_number', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=255)),
                ('applicant_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BasicInfo',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='basic_info', serialize=False, to='bkend.registration')),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=20)),
                ('religion', models.CharField(max_length=50)),
                ('marital_status', models.CharField(max_length=20)),
                ('birthdate', models.DateField()),
                ('country_of_birth', models.CharField(max_length=100)),
                ('siblings_count', models.PositiveIntegerField()),
                ('nationality', models.CharField(max_length=100)),
                ('skype_account', models.CharField(blank=True, max_length=100, null=True)),
                ('transferring_institution', models.BooleanField(default=False)),
                ('disability_info', models.TextField(blank=True, null=True)),
                ('allergies_info', models.TextField(blank=True, null=True)),
                ('passport_issue_date', models.DateField()),
                ('passport_issue_place', models.CharField(max_length=100)),
                ('has_malaysian_pass', models.BooleanField(default=False)),
                ('passport_expiry_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Basic Information',
                'verbose_name_plural': 'Basic Information Records',
            },
        ),
        migrations.CreateModel(
            name='ProgramSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_program', models.CharField(max_length=255)),
                ('second_program', models.CharField(blank=True, max_length=255, null=True)),
                ('third_program', models.CharField(blank=True, max_length=255, null=True)),
                ('fourth_program', models.CharField(blank=True, max_length=255, null=True)),
                ('intake_year', models.CharField(max_length=50)),
                ('study_mode', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bkend.registration')),
            ],
        ),
    ]
