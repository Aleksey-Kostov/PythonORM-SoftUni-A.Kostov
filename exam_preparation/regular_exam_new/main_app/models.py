from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator


class Author(models.Model):
    full_name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveIntegerField(validators=[MaxValueValidator(2005), MinValueValidator(1900)])
    website = models.URLField(blank=True, null=True)


class Article(models.Model):
    class CategoryChoice(models.TextChoices):
        TECHNOLOGY = 'Technology', 'Technology'
        SCIENCE = 'Science', 'Science'
        EDUCATION = 'Education', 'Education'

    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    content = models.TextField(validators=[MinLengthValidator(10)])
    category = models.CharField(choices=CategoryChoice, max_length=10, default='Technology')
    authors = models.ManyToManyField(Author, related_name='author_articles')
    published_on = models.DateTimeField(auto_now_add=True, editable=False)


class Review(models.Model):
    content = models.TextField(validators=[MinLengthValidator(10)])
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author_reviews")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_reviews")
    published_on = models.DateTimeField(auto_now_add=True, editable=False)
