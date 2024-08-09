from django.utils import timezone
import re
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.custom_manager import HouseManager


class House(models.Model):
    name = models.CharField(max_length=80, validators=[MinLengthValidator(5)], unique=True)
    motto = models.TextField(null=True, blank=True)
    is_ruling = models.BooleanField(default=False)
    castle = models.CharField(max_length=80, null=True, blank=True)
    wins = models.PositiveSmallIntegerField(default=0)
    modified_at = models.DateTimeField(auto_now=True)

    objects = HouseManager()

    def __str__(self):
        return self.name


class Dragon(models.Model):
    class BreathChoices(models.TextChoices):
        FIRE = 'Fire', 'Fire'
        ICE = 'Ice', 'Ice'
        LIGHTNING = 'Lightning', 'Lightning'
        UNKNOWN = 'Unknown', 'Unknown'

    name = models.CharField(max_length=80, validators=[MinLengthValidator(5)], unique=True)
    power = models.DecimalField(max_digits=3, decimal_places=1,
                                validators=[MaxValueValidator(10.0), MinValueValidator(1.0)], default=1.0)
    breath = models.CharField(choices=BreathChoices, default='Unknown', max_length=9)
    is_healthy = models.BooleanField(default=True)
    birth_date = models.DateField(default=timezone.now)
    wins = models.PositiveSmallIntegerField(default=0)
    modified_at = models.DateTimeField(auto_now=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='house_dragons')

    def __str__(self):
        return self.name


class Quest(models.Model):
    def validate_code(value):
        if len(value) != 4:
            raise ValidationError('Code must contain exactly 4 characters.')
        if not re.match('^[A-Za-z#]{4}$', value):
            raise ValidationError('Code must only contain letters (A-Z, a-z) and the hash symbol "#".')

    name = models.CharField(max_length=80, validators=[MinLengthValidator(5)], unique=True)
    code = models.CharField(max_length=4,
                            validators=[validate_code])
    reward = models.FloatField(default=100.0)
    start_time = models.DateTimeField()
    modified_at = models.DateTimeField(auto_now=True)
    dragons = models.ManyToManyField(Dragon, related_name='dragons_quest')
    host = models.ForeignKey(House, on_delete=models.CASCADE, related_name='host_quests')



    def __str__(self):
        return self.name
