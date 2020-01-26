from django.contrib.gis.db.models.functions import Distance
from django.db.models import IntegerField, Case, F, Value, When, Q
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from cities.models import City
from rest_framework import permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

import logging

from .models import Tip
from .permissions import IsOwnerOrReadOnly
from .serializers import TipSerializer
from .serializers import CityNestedSerializer

logger = logging.getLogger(__name__)

class TipViewSet(viewsets.ModelViewSet):
    queryset = Tip.objects.all().order_by('-score')
    serializer_class = TipSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        longitude = self.request.query_params.get('longitude', None)
        latitude = self.request.query_params.get('latitude', None)

        global_tips = Tip.objects.filter(
            Q(cities=None) &
            Q(subregions=None) &
            Q(regions=None) &
            Q(countries=None)
        ).distinct()

        if not (longitude and latitude):
            queryset = global_tips
            closest_city = None
        else:
            location = Point(float(longitude), float(latitude))
            close_cities = City.objects.filter(
                    location__distance_lte=(location, D(km=50))).annotate(
                            distance=Distance('location', location))

            close_cities = close_cities.order_by('distance')[:10]
            closest_city = close_cities.first()
            close_cities = close_cities[1:]
            logger.debug("Looking tips in nearby cities %s", close_cities)
            logger.debug("Closest city is %s", closest_city)

            local_tips = Tip.objects.filter(
                Q(cities=closest_city) |
                Q(cities__in=close_cities) |
                Q(subregions=closest_city.subregion) |
                Q(regions=closest_city.region) |
                Q(countries=closest_city.region.country)
            ).distinct()

            queryset = (local_tips | global_tips).distinct()

        if closest_city:
            queryset = queryset.annotate(
                closest_city_score=Case(
                    When(cities=closest_city,
                         then=(F('score') + 1) * 200),
                    default=0,
                    output_field=IntegerField()),

                close_cities_score=Case(
                    When(cities__in=close_cities,
                         then=(F('score') + 1) * 100),
                    default=0,
                    output_field=IntegerField()),

                close_subregions_score=Case(
                    When(subregions=closest_city.subregion,
                         then=(F('score') + 1) * 50),
                    default=0,
                    output_field=IntegerField()),

                close_regions_score=Case(
                    When(regions=closest_city.region,
                         then=(F('score') + 1) * 20),
                    default=0,
                    output_field=IntegerField()),

                close_countries_score=Case(
                    When(countries=closest_city.region.country,
                         then=(F('score') + 1) * 10),
                    default=0,
                    output_field=IntegerField()))

            queryset = queryset.annotate(
                boost_score=(F('score') + F('closest_city_score') +
                             F('close_cities_score') +
                             F('close_subregions_score') +
                             F('close_regions_score') +
                             F('close_countries_score'))
                )

            return queryset.order_by('-boost_score', 'id').prefetch_related(
                'cities', 'subregions', 'regions', 'countries').distinct()
        else:
            return queryset.order_by('-score').distinct()


class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CityNestedSerializer
    queryset = City.objects.all()

    def get_queryset(self):
        longitude = self.request.query_params.get('longitude', None)
        latitude = self.request.query_params.get('latitude', None)
        cities = City.objects.all()
        if longitude and latitude:
            location = Point(float(longitude), float(latitude))
            cities = City.objects.filter(
                    location__distance_lte=(location, D(km=100))).annotate(
                            distance=Distance('location', location))
            cities = cities.order_by('distance')
        return cities
