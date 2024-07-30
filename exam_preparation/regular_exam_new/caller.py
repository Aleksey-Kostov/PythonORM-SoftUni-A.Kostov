import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author
from django.db.models import Q, Count


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''

    if search_name is not None and search_email is not None:
        authors = (Author.objects.filter(full_name__icontains=search_name, email__icontains=search_email)
                   .order_by('-full_name'))
    elif search_name is not None:
        authors = Author.objects.filter(full_name__icontains=search_name).order_by('-full_name')

    else:
        authors = Author.objects.filter(email__icontains=search_email).order_by('-full_name')

    if authors:
        result = []
        [result.append(f"Author: {a.full_name}, email: {a.email}, "
                       f"status: {'Banned' if a.is_banned == True else 'Not Banned'}") for a in authors]
        return '\n'.join(result)

    else:
        return ''


def get_top_publisher():
    author = Author.objects.get_authors_by_article_count().first()

    if author is None or author.article_count == 0:
        return ''

    return f"Top Author: {author.full_name} with {author.article_count} published articles."


def get_top_reviewer():
    author = (Author.objects.annotate(review_count=Count('author_reviews')).order_by('-review_count', 'email')
              .first())

    if author is None or author.review_count == 0:
        return ''

    return f"Top Reviewer: {author.full_name} with {author.review_count} published reviews."

