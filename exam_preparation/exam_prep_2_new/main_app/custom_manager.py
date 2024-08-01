from django.db import models
from django.db.models import Count


class ProfileManager(models.Manager):
    def get_regular_customers(self):
        return (self.annotate(num_orders=Count('profile_orders'), num_status=Count('profile_orders__is_completed')).
                filter(num_orders__gt=2).order_by('-num_orders'))
