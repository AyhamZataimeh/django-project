# Generated by Django 3.2.8 on 2022-01-10 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_requested_book'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Requested_Book',
            new_name='RequestedBook',
        ),
    ]
