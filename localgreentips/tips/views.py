from django.contrib.gis.db.models.functions import Distance
from django.db.models import IntegerField, Case, F, Value, When
from django.contrib.gis.geos import Point 
from django.contrib.gis.measure import D
from cities.models import City
from rest_framework import viewsets

from .models import Tip, Tipper
from .serializers import TipSerializer, TipperSerializer


class TipViewSet(viewsets.ModelViewSet):
    queryset = Tip.objects.all().order_by('-score')
    serializer_class = TipSerializer

    def get_queryset(self):
        longitude = self.request.query_params.get('longitude', None)
        latitude= self.request.query_params.get('latitude', None)

        global_tips = Tip.objects.filter(
                cities=None,
                regions=None,
                countries=None)

        if not (longitude and latitude):
            queryset = global_tips
            closest_city = None
        else:
            location = Point(float(longitude), float(latitude))
            close_cities = City.objects.filter(
                    location__distance_lte=(location, D(km=10))).annotate(
                            distance=Distance('location', location))

            closest_city = close_cities.order_by('distance')[:1][0]

            local_tips = Tip.objects.filter(
                    cities=closest_city,
                    regions=closest_city.region,
                    countries=closest_city.region.country
                    )

            queryset = local_tips | global_tips

        if closest_city:
            queryset = queryset.annotate(
                boost_score=Case(
                    When(cities=closest_city, then=F('score') * 1000),
                    When(regions=closest_city.region, then=F('score') * 100),
                    When(countries=closest_city.region.country, then=F('score') * 10),
                    default=F('score'),
                    output_field=IntegerField()))

            return queryset.order_by('-boost_score').prefetch_related('cities', 'regions', 'countries')
        else:
            return queryset.order_by('-score')


class TipperViewSet(viewsets.ModelViewSet):
    queryset = Tipper.objects.all()
    serializer_class = TipperSerializer
