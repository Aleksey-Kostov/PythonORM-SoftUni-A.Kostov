import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Book


def show_all_authors_with_their_books() -> str:
    authors_with_books = []

    authors = Author.objects.all().order_by("id")  # select prefetch prefetch_related

    for author in authors:
        books = Book.objects.filter(author=author)
        # books = author.book_set.all() option 2

        if not books:
            continue

        titles = ", ".join(b.title for b in books)
        authors_with_books.append(
            f"{author.name} has written - {titles}!"
        )

    return "\n".join(authors_with_books)


def delete_all_authors_without_books() -> None:
    Author.objects.filter(book__isnull=True).delete()
