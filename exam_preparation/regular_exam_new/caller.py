import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Article
from django.db.models import Q, Count, Avg


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


def get_latest_article():
    articles = (Article.objects.prefetch_related('authors', 'article_reviews')
                .annotate(num_reviews=Count('article_reviews'), avg_rating=Avg('article_reviews__rating'))
                .order_by('-published_on')
                .first())
    if articles is None:
        return ''

    rating = articles.avg_rating or 0.0

    articles_authors_full_name = ', '.join(a.full_name for a in articles.authors.all().order_by('full_name'))

    return (f"The latest article is: {articles.title}. Authors: {articles_authors_full_name}. "
            f"Reviewed: {articles.num_reviews} times. Average Rating: {rating:.2f}.")

# print(get_latest_article())

def get_top_rated_article():
    top_article = (Article.objects.prefetch_related('article_reviews')
                   .annotate(avg_rating=Avg('article_reviews__rating'), num_reviews=Count('article_reviews'))
                   .order_by('-avg_rating', 'title').first())

    if top_article is None or top_article.num_reviews == 0:
        return ''

    # avg_rating = top_article.avg_rating or 0.0

    return (f"The top-rated article is: {top_article.title}, with an average rating of {top_article.avg_rating:.2f}, "
            f"reviewed {top_article.num_reviews} times.")


# print(get_top_rated_article())
def ban_author(email=None):
    if email is None:
        return 'No authors banned.'

    author = (Author.objects.prefetch_related('author_reviews').annotate(num_reviews=Count('author_reviews')).
              filter(email__exact=email).first())

    if author is None:
        return 'No authors banned.'

    author.is_banned = True
    author.save()
    author.author_reviews.all().delete()
    return f"Author: {author.full_name} is banned! {author.num_reviews} reviews deleted."

# print(ban_author('kolio'))
