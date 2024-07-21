from django.db import models


class AuthorManager(models.Manager):
    def get_authors_by_article_count(self):
        return self.annotate(article_count=models.Count('articles')).order_by('-article_count', 'email')
