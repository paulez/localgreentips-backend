from rest_framework import serializers

from cities.models import Country, Region, City

from .models import Tip, Tipper, Comment

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('name',)

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ('name',)

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('name',)

class TipSerializer(serializers.ModelSerializer):
    
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

