# Generated by Django 3.2.8 on 2021-11-19 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_blockusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockusers',
            name='profile_image',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.profileimage'),
        ),
    ]