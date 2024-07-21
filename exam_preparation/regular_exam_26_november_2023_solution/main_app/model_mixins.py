from django.core.validators import MinLengthValidator
from django.db import models


class ContentFieldMixin(models.Model):
    content = models.TextField(validators=[MinLengthValidator(10)])

    class Meta:
        abstract = True


class PublishedOnFieldMixin(models.Model):
    published_on = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True
