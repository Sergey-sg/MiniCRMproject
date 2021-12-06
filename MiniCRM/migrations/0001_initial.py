# Generated by Django 3.2.9 on 2021-12-06 15:14

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('description', ckeditor.fields.RichTextField(blank=True, help_text='Company description', null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('contact_person', models.CharField(help_text='Full name of the contact person', max_length=450)),
                ('position_person', models.CharField(help_text='Position of the contact person', max_length=300)),
                ('address', models.CharField(blank=True, help_text='Company address', max_length=250)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='add_company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('description', ckeditor.fields.RichTextField(blank=True, help_text='Project description', null=True)),
                ('start_dates', models.DateField(blank=True, help_text='Enter the date of start project', null=True)),
                ('deadline', models.DateField(blank=True, help_text='Enter the date of deadline', null=True)),
                ('price', models.DecimalField(decimal_places=2, help_text='Enter price project', max_digits=10)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='MiniCRM.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='add_project', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, help_text='Phone number must be in format: "+380999999999"', max_length=13, validators=[django.core.validators.RegexValidator(message='Phone number must be in format: "+380999999999". Up to "+380" and 9 digits.', regex='^\\+380\\d{9}')])),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='MiniCRM.company')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', ckeditor.fields.RichTextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MiniCRM.company')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MiniCRM.projectcompany')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='add_message', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='Like')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MiniCRM.message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='add_like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InteractionInformationCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_interaction', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MiniCRM.company')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MiniCRM.projectcompany')),
            ],
        ),
        migrations.CreateModel(
            name='EmailCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MiniCRM.company')),
            ],
        ),
    ]
