from django.db import models


class BaseCharacter(models.Model):
    class Meta:
        abstract = True
    name = models.CharField(max_length=100)
    description = models.TextField()


class Mage(BaseCharacter):
    elemental_power = models.CharField(max_length=100)
    spellbook = models.CharField(max_length=100)
