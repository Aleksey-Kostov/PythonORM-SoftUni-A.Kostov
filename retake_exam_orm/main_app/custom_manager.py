from django.db import models


class HouseManager(models.Manager):
    def get_houses_by_dragons_count(self):
        return self.annotate(dragons_count=models.Count('house_dragons')).order_by('-dragons_count', 'name')
