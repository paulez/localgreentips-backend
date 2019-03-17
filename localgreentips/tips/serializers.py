from rest_framework import serializers

from cities_light.models import Country, Region, City
from cities_light.contrib.restframework3 import CitySerializer, RegionSerializer, CountrySerializer

from .models import Tip, Tipper, Comment


class TipSerializer(serializers.HyperlinkedModelSerializer):

    cities = CitySerializer(many=True, required=False)
    regions = RegionSerializer(many=True, required=False)
    countries = CountrySerializer(many=True, required=False)

    class Meta:
        model = Tip
        fields = ('title', 'user', 'text', 'score', 'cities', 'regions', 'countries')

class TipperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tipper
        fields = ('user',)

