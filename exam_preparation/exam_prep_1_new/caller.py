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
        directors = (Director.objects
                     .filter(full_name__icontains=search_name, nationality__icontains=search_nationality)
                     .order_by('full_name'))

    elif search_name:
        directors = (Director.objects
                     .filter(full_name__icontains=search_name)
                     .order_by('full_name'))

    else:
        directors = (Director.objects
                     .filter(nationality__icontains=search_nationality)
                     .order_by('full_name'))

    if directors is None:
        return ''

    result = []

    [result.append(f"Director: {d.full_name}, "
                   f"nationality: {d.nationality}, "
                   f"experience: {d.years_of_experience}") for d in directors]

    return '\n'.join(result)


def get_top_director():
    director = Director.objects.get_directors_by_movies_count()

    if director is None:
        return ''

    return f"Top Director: {director.full_name}, movies: {director.num_movies}."


def get_top_actor():
    actors = (Actor.objects.prefetch_related('starring_actor_movies')
              .annotate(num_starring=Count('starring_actor_movies'),
                        movies_avg_rating=Avg('starring_actor_movies__rating'))
              .order_by('-num_starring', 'full_name')
              .first())
    if not actors or not actors.num_starring:
        return ''

    movies_title = ', '.join(a.title for a in actors.starring_actor_movies.all() if a)

    return (f"Top Actor: {actors.full_name}, "
            f"starring in movies: {movies_title}, "
            f"movies average rating: {actors.movies_avg_rating:.1f}")
