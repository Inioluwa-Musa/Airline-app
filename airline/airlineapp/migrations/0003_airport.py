# Generated by Django 5.1.4 on 2024-12-23 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airlineapp', '0002_rename_airlineapp_flight'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('city', models.CharField(max_length=64)),
            ],
        ),
    ]
