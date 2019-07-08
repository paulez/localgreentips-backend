from django.db import models
from django.contrib.auth.models import User
from cities.models import Country, Region, City

class Tip(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    score = models.IntegerField()
    tipper = models.ForeignKey(
        'auth.User',
        related_name='snippets',
        on_delete=models.SET_NULL,
        null=True,
    )

    cities = models.ManyToManyField(City, blank=True)
    regions = models.ManyToManyField(Region, blank=True)
    countries = models.ManyToManyField(Country, blank=True)

    def __str__(self):
        return "{} by {}".format(self.title, self.user)


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(
            'auth.User',
            on_delete=models.CASCADE,
            null=True,
    )
