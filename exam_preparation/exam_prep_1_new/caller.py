import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor, Movie
from django.db.models import Count, Avg, F


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
    director = Director.objects.get_directors_by_movies_count().first()

    if director is None:
        return ''

    return f"Top Director: {director.full_name}, movies: {director.num_movies}."


def get_top_actor():
    actors = (Actor.objects.prefetch_related('starring_actor_movies')
              .annotate(num_starring=Count('starring_actor_movies'),
                        movies_avg_rating=Avg('starring_actor_movies__rating'))
              .order_by('-num_starring', 'full_name').first())
    if actors is None or not actors.num_starring:
        return ''

    movies_title = ', '.join(movie.title for movie in actors.starring_actor_movies.all() if movie)

    return (f"Top Actor: {actors.full_name}, starring in movies: {movies_title}, "
            f"movies average rating: {actors.movies_avg_rating:.1f}")


def get_actors_by_movies_count():
    actors = (Actor.objects.prefetch_related('actors_movies')
              .annotate(num_movies=Count('actors_movies'))
              .order_by('-num_movies', 'full_name')[:3])

    if not actors or actors[0].num_movies == 0:
        return ''

    result = []

    [result.append(f"{a.full_name}, participated in {a.num_movies} movies") for a in actors]

    return '\n'.join(result)


# print(get_actors_by_movies_count())


def get_top_rated_awarded_movie():
    movie = (Movie.objects.select_related('starring_actor')
             .prefetch_related('actors')
             .filter(is_awarded=True).order_by('-rating')
             .first())

    if movie is None:
        return ""

    starring_actor_full_name = 'N/A' if movie.starring_actor is None else movie.starring_actor.full_name
    actors = ', '.join(a.full_name for a in movie.actors.order_by('full_name').all())

    return (f"Top rated awarded movie: {movie.title}, "
            f"rating: {movie.rating}. "
            f"Starring actor: {starring_actor_full_name}. "
            f"Cast: {actors}.")


# print(get_top_rated_awarded_movie())
def increase_rating():
    movies = Movie.objects.filter(is_classic=True, rating__lt=10)

    if not movies:
        return 'No ratings increased.'

    num_of_updated_movies = movies.count()
    movies.update(rating=F("rating") + 0.1)

    return f'Rating increased for {num_of_updated_movies} movies.'
