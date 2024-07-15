# Generated by Django 5.0.4 on 2024-07-15 19:50

import django.contrib.postgres.search
import django.core.validators
import main_app.mixins
import main_app.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('genre', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(5, 'Author must be at least 5 characters long')])),
                ('isbn', models.CharField(max_length=20, unique=True, validators=[django.core.validators.MinLengthValidator(6, 'ISBN must be at least 6 characters long')])),
            ],
            options={
                'verbose_name': 'Model Book',
                'verbose_name_plural': 'Models of type - Book',
                'ordering': ['-created_at', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[main_app.validators.ValidateName('Name can only contain letters and spaces')])),
                ('age', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(18, message='Age must be greater than or equal to 18')])),
                ('email', models.EmailField(error_messages={'invalid': 'Enter a valid email address'}, max_length=254)),
                ('phone_number', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message="Phone number must start with '+359' followed by 9 digits", regex='^\\+359\\d{9}$')])),
                ('website_url', models.URLField(error_messages={'invalid': 'Enter a valid URL'})),
            ],
        ),
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('hero_title', models.CharField(max_length=100)),
                ('energy', models.PositiveIntegerField()),
            ],
            bases=(models.Model, main_app.mixins.RechargeEnergyMixin),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('genre', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('director', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(8, 'Director must be at least 8 characters long')])),
            ],
            options={
                'verbose_name': 'Model Movie',
                'verbose_name_plural': 'Models of type - Movie',
                'ordering': ['-created_at', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('genre', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('artist', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(9, 'Artist must be at least 9 characters long')])),
            ],
            options={
                'verbose_name': 'Model Music',
                'verbose_name_plural': 'Models of type - Music',
                'ordering': ['-created_at', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
            ],
            options={
                'indexes': [models.Index(fields=['search_vector'], name='main_app_do_search__c97410_idx')],
            },
        ),
        migrations.CreateModel(
            name='FlashHero',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main_app.hero',),
        ),
        migrations.CreateModel(
            name='SpiderHero',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main_app.hero',),
        ),
        migrations.CreateModel(
            name='DiscountedProduct',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main_app.product',),
        ),
    ]
