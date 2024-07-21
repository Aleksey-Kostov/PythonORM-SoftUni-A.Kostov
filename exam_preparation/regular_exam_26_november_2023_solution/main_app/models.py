# Create your models here.
from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

from main_app.custom_model_manager import AuthorManager
from main_app.model_mixins import ContentFieldMixin, PublishedOnFieldMixin


class Author(models.Model):
    full_name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2005)])
    website = models.URLField(blank=True, null=True)

    objects = AuthorManager()

    def __str__(self):
        return self.full_name


class Article(ContentFieldMixin, PublishedOnFieldMixin, models.Model):
    CATEGORIES = [
        ('Technology', 'Technology'),
        ('Science', 'Science'),
        ('Education', 'Education')
    ]

    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    category = models.CharField(max_length=10, choices=CATEGORIES, default='Technology')
    authors = models.ManyToManyField(Author, related_name='articles')

    def __str__(self):
        return self.title


class Review(ContentFieldMixin, PublishedOnFieldMixin, models.Model):
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='reviews')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"Review for '{self.article.title}' by {self.author.full_name}"
