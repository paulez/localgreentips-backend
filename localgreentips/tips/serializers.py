from rest_framework import serializers

from cities.models import Country, Region, City

from .models import Tip, Tipper, Comment


class TipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tip
        fields = ('title', 'user', 'text', 'score', 'cities', 'regions', 'countries')

class TipperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tipper
        fields = ('user',)

