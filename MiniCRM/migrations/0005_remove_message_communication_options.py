# Generated by Django 3.2.9 on 2021-12-08 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MiniCRM', '0004_auto_20211208_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='communication_options',
        ),
    ]