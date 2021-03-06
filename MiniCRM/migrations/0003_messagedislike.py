# Generated by Django 3.2.10 on 2021-12-15 07:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MiniCRM', '0002_alter_user_user_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageDisLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dislike', models.BooleanField(default=False, verbose_name='DisLike')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('disliked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MiniCRM.message')),
            ],
        ),
    ]
