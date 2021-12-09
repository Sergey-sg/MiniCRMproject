# Generated by Django 3.2.9 on 2021-12-08 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MiniCRM', '0006_delete_communication'),
    ]

    operations = [
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('communication', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='communication_options',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MiniCRM.communication'),
        ),
    ]