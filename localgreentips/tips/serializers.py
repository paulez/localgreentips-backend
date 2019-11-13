import logging

from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cities.models import Country, Region, Subregion, City

from .models import Tip, Comment

logger = logging.getLogger(__name__)

class CitySerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = City
        fields = ('id', 'name',)

class RegionSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = Region
        fields = ('id', 'name',)

class SubregionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Subregion
        fields = ('id', 'name',)

class CountrySerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = Country
        fields = ('id', 'name',)

class RegionNestedSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    country = CountrySerializer()

    class Meta:
        model = Region
        fields = ('id', 'name', 'country')

class SubregionNestedSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    region = RegionNestedSerializer()

    class Meta:
        model = Subregion
        fields = ('id', 'name', 'region')

class CityNestedSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    subregion = SubregionSerializer()
    region = RegionSerializer()
    country = CountrySerializer()

    class Meta:
        model = City
        fields = ('id', 'name', 'subregion', 'region', 'country')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }

class TipSerializer(serializers.ModelSerializer):

    cities = CitySerializer(many=True, required=False)
    regions = RegionSerializer(many=True, required=False)
    subregions = SubregionSerializer(many=True, required=False)
    countries = CountrySerializer(many=True, required=False)
    tipper = UserSerializer(required=False, read_only=True)
    score = serializers.FloatField(required=False, read_only=True)

    class Meta:
        model = Tip
        fields = ('id', 'title', 'tipper', 'text',
                  'score', 'cities', 'regions', 'subregions', 'countries')

    def create(self, validated_data):
        logger.debug("Creating tip. Validated data: %s", validated_data)

        def get_related(model, name):
            try:
                data = validated_data.pop(name)
            except KeyError:
                data = []
            related = []

            for item in data:
                related_item = model.objects.get(pk=item["id"])
                if related_item.name != item["name"]:
                    raise ValidationError(
                        "id and name don't match for {}".format(item["name"]))
                related.append(related_item)
            return related

        cities = get_related(City, "cities")
        regions = get_related(Region, "regions")
        countries = get_related(Country, "countries")

        tipper_username = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            tipper_username = request.user
        logger.debug("Retrieving tipper: %s", tipper_username)
        tipper = User.objects.get(username=tipper_username)

        tip = Tip.objects.create(tipper=tipper,
                                 score=0.0,
                                 **validated_data)

        tip.cities.set(cities)
        tip.regions.set(regions)
        tip.countries.set(countries)

        return tip
