# Generated by Django 3.1.5 on 2021-01-17 01:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plaidkey',
            name='user',
        ),
        migrations.AlterField(
            model_name='plaidkey',
            name='access_token',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='access_token', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='plaidkey',
            name='item_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='item_id', to=settings.AUTH_USER_MODEL),
        ),
    ]