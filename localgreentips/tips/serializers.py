from django.contrib.auth.models import User
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

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)

class TipperSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = Tipper
        fields = ('user',)

class TipSerializer(serializers.ModelSerializer):
    
    cities = serializers.StringRelatedField(many=True, required=False)
    regions = serializers.StringRelatedField(many=True, required=False)
    countries = serializers.StringRelatedField(many=True, required=False)
    tipper = serializers.StringRelatedField()

    class Meta:
        model = Tip
        fields = ('title', 'tipper', 'text', 'score', 'cities', 'regions', 'countries')

class TipperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tipper
        fields = ('user',)

