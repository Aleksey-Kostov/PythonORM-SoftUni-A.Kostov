# Generated by Django 5.0.4 on 2024-07-22 18:23

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='author',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
