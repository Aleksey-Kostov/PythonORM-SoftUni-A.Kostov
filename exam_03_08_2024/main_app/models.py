from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.custom_manager import AstronautManager


class Astronaut(models.Model):

    def only_int(value):
        if not value.isdigit():
            raise ValidationError('ID contains characters')

    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    phone_number = models.CharField(max_length=15, unique=True, validators=[only_int])
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank=True)
    spacewalks = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    updated_at = models.DateTimeField(auto_now=True)

    objects = AstronautManager()

    def __str__(self):
        return self.name


class Spacecraft(models.Model):
    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    manufacturer = models.CharField(max_length=100)
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    weight = models.FloatField(validators=[MinValueValidator(0.0)])
    launch_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Mission(models.Model):
    class StatusChoices(models.TextChoices):
        PLANNED = 'Planned', 'Planned'
        ONGOING = 'Ongoing', 'Ongoing'
        COMPLETED = 'Completed', 'Completed'

    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    description = models.TextField(null=True, blank=True)
    status = models.CharField(choices=StatusChoices, default='Planned', max_length=9)
    launch_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE, related_name='spacecraft_missions')
    astronauts = models.ManyToManyField(Astronaut, related_name='astronauts_missions')
    commander = models.ForeignKey(Astronaut, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='commander_missions')
