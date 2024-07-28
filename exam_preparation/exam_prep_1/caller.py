import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor, Movie
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


def get_actors_by_movies_count():
    top_actors = (Actor.objects.prefetch_related('actor_movies').annotate(num_movies=Count('actor_movies'))
                  .order_by('-num_movies', 'full_name'))[:3]

    if not top_actors or not top_actors.num_movies:
        return ''

    result = []

    [result.append(f"{a.full_name}, participated in {a.num_movies} movies") for a in top_actors]

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    top_movie = (Movie.objects.select_related('starring_actor').prefetch_related('actors')
                 .filter(is_awarded=True).order_by('-rating', 'title').first())

    if top_movie is None:
        return ""

    starring_actor_full_name = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'

    cast_actor = top_movie.actors.order_by('full_name').values_list('full_name', flat=True)
    cast = ', '.join(cast_actor)

    return (f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating}. "
            f"Starring actor: {starring_actor_full_name}. "
            f"Cast: {cast}.")


