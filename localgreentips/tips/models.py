from django.db import models
from django.contrib.auth.models import User
from cities.models import Country, Region, City

class Tipper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Tip(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    score = models.IntegerField()

    tipper = models.ForeignKey(
            Tipper,
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
            Tipper,
            on_delete=models.SET_NULL,
            null=True,
    )
