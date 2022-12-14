# Generated by Django 4.0.7 on 2022-08-08 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_activation_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='activation_link',
        ),
        migrations.CreateModel(
            name='ActivationLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_link', models.CharField(default='create_activation_link', max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
