# Generated by Django 3.2.8 on 2022-01-10 22:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_rename_product_requestedbook_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestedbook',
            old_name='user',
            new_name='product_owner',
        ),
        migrations.RemoveField(
            model_name='requestedbook',
            name='email',
        ),
        migrations.RemoveField(
            model_name='requestedbook',
            name='username',
        ),
        migrations.AddField(
            model_name='requestedbook',
            name='requetd_user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
