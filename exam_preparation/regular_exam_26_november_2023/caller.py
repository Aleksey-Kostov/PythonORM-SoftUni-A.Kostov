import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Review
from django.db.models import Count


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''

    if search_name is not None and search_email is not None:
        authors = (Author.objects.filter
                   (full_name__icontains=search_name, email__icontains=search_email).order_by('-full_name'))

    elif search_name is not None:
        authors = Author.objects.fiilter(full_name__icontains=search_name).order_by('-full_name')

    else:
        authors = Author.objects.fiilter(email__icontains=search_email).order_by('-full_name')

    result = []

    [result.append(f"Author: {a.full_name}, email: {a.mail}, status: {'Banned' if a.is_banned else 'Not Banned'}")
     for a in authors if authors]

    return "\n".join(result) if result else ""


def get_top_publisher():
    author = Author.objects.get_authors_by_article_count.first()
    if author is None or author.article_count == 0:
        return ""

    return f"Top Author: {author.full_name} with {author.article_count} published articles."


def get_top_reviewer():
    author_review = Author.objects.annotate(num_review=Count('reviews')).order_by('-num_review', 'email').first()
    if author_review is None or author_review.num_review == 0:
        return ''
    return f"Top Reviewer: {author_review.full_name} with {author_review.num_review} published reviews."
