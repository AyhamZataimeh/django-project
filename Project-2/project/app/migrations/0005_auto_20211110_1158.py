# Generated by Django 3.2.8 on 2021-11-10 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_products_is_booked'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='products',
            name='is_pending',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='products',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]