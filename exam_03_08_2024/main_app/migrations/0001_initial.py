# Generated by Django 5.0.4 on 2024-08-03 11:36

import django.core.validators
import django.db.models.deletion
import main_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Astronaut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, validators=[django.core.validators.MinLengthValidator(2)])),
                ('phone_number', models.CharField(max_length=15, unique=True, validators=[main_app.models.Astronaut.only_int])),
                ('is_active', models.BooleanField(default=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('spacewalks', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Spacecraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, validators=[django.core.validators.MinLengthValidator(2)])),
                ('manufacturer', models.CharField(max_length=100)),
                ('capacity', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('weight', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('launch_date', models.DateField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, validators=[django.core.validators.MinLengthValidator(2)])),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Planned', 'Planned'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed')], default='Planned', max_length=9)),
                ('launch_date', models.DateField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('astronauts', models.ManyToManyField(related_name='astronauts_missions', to='main_app.astronaut')),
                ('commander', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commander_missions', to='main_app.astronaut')),
                ('spacecraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spacecraft_missions', to='main_app.spacecraft')),
            ],
        ),
    ]
