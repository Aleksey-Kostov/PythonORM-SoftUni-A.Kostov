# Generated by Django 5.0.4 on 2024-07-28 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='is_activ',
            new_name='is_active',
        ),
    ]
