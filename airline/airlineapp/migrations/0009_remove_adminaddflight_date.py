# Generated by Django 5.1.4 on 2024-12-24 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airlineapp', '0008_adminaddflight_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminaddflight',
            name='date',
        ),
    ]