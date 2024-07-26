# Generated by Django 5.0.4 on 2024-07-26 18:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_actor_last_updated_alter_movie_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3, validators=[django.core.validators.MaxValueValidator(10.0), django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
