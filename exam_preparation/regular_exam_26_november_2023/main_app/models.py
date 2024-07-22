from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models


class Author(models.Model):
    full_name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2005)])
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.full_name


class Article(models.Model):
    class ArticleCategory(models.TextChoices):
        TECHNOLOGY = 'Technology', 'Technology'
        SCIENCE = 'Science', 'Science'
        EDUCATION = 'Education', 'Education'

    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    content = models.TextField(validators=[MinLengthValidator(10)])
    category = models.CharField(choices=ArticleCategory, default='Technology', max_length=10)
    authors = models.ManyToManyField(Author, related_name='article')
    published_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title


class Review(models.Model):
    content = models.TextField(validators=[MinLengthValidator(10)])
    rating = models.FloatField(validators=[MinValueValidator(1.0)], max_length=5.0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='reviews')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reviews')
    published_on = models.DateTimeField(auto_now_add=True, editable=False)
