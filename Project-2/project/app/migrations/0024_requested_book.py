# Generated by Django 3.2.8 on 2022-01-10 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_rename_total_post_useraccount_total_posts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requested_Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=80)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.products')),
            ],
        ),
    ]
