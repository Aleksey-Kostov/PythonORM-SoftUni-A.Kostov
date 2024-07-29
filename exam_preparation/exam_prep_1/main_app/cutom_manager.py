from django.db import models
from django.db.models import Count


class DirectorManager(models.Manager):
    def get_directors_by_movies_count(self):
        return self.annotate(num_director=Count('director_movies')).order_by('-num_director', 'full_name')