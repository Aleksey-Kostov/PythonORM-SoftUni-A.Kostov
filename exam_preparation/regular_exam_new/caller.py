import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author
from django.db.models import Q


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''

    authors = (Author.objects.filter(Q(full_name__icontains=search_name) | Q(email__icontains=search_email))
               .order_by('-full_name'))

    if authors is None:
        return ""

    result = []

    [result.append(f"Author: {a.full_name}, email: {a.email}, "
                   f"status: {'Banned' if a.is_banned == True else 'Not Banned'}") for a in authors]

    return '\n'.join(result)


def get_top_publisher():
    author = Author.objects.get_authors_by_article_count().first()

    if author.article_count == 0:
        return ''

    return f"Top Author: {author.full_name} with {author.article_count} published articles."


def get_top_reviewer():
    author = Author.objects.annotate(review_count='author_reviews').order_by('-review_count', 'email').first()

    if author.review_count == 0:
        return ''

    return f"Top Reviewer: {author.full_name} with {author.review_count} published reviews"
