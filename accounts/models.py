from django.contrib.auth.models import AbstractUser
from django.db import models

from multiselectfield import MultiSelectField


CHOICES = (
    ('1', 'Programming'),
    ('2', 'Food'),
    ('3', 'Beauty'),
    ('4', 'Plants')
)   # TODO: Solve the fucking categories


class User(AbstractUser):
    is_blogger = models.BooleanField(default=False)
    is_reader = models.BooleanField(default=False)


class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    interests = MultiSelectField(choices=CHOICES, null=True, blank=True)
    is_adult = models.BooleanField(default=False, null=True, blank=True)


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    categories = MultiSelectField(choices=CHOICES, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
