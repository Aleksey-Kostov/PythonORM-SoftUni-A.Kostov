import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor
from django.db.models import Count, Avg


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''
    if search_name is not None and search_nationality is not None:
        directors = Director.objects.filter(full_name__icontains=search_name,
                                            nationality__icontains=search_nationality).order_by('full_name')

    elif search_name is not None:
        directors = Director.objects.filter(full_name__icontains=search_name).order_by('full_name')

    else:
        directors = Director.objects.filter(nationality__icontains=search_nationality).order_by('full_name')

    if not directors:
        return ''

    result = []

    [result.append(f"Director: {d.full_name}, nationality: "
                   f"{d.nationality}, experience: {d.years_of_experience}") for d in directors]

    return '\n'.join(result)


def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()

    if not director:
        return ""

    return f"Top Director: {director.full_name}, movies: {director.num_director}."


def get_top_actor():
    actor = ((Actor.objects.prefetch_related('starring_movies')
              .annotate(num_starring=Count('starring_movies'),
                        movies_avg_rating=Avg('starring_movies__rating')))
             .order_by('-num_starring', 'full_name')
             .first())
    if not actor or not actor.num_starring:
        return ''

    movies_title = ', '.join(movie.title for movie in actor.starring_movies.all() if movie)

    return (f"Top Actor: {actor.full_name}, starring in movies: {movies_title}, "
            f"movies average rating: {actor.movies_avg_rating:.1f}")
