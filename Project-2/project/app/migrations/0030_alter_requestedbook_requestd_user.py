# Generated by Django 3.2.8 on 2022-01-11 00:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20220111_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestedbook',
            name='requestd_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]