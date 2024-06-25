# Generated by Django 5.0.4 on 2024-06-25 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('duration_minutes', models.PositiveIntegerField()),
                ('difficulty_level', models.CharField(max_length=20)),
                ('equipment', models.CharField(max_length=90)),
                ('video_url', models.URLField(blank=True, null=True)),
                ('calories_burned', models.PositiveIntegerField(default=1)),
                ('is_favorite', models.BooleanField(default=False)),
            ],
        ),
    ]
