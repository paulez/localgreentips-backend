from django.contrib.gis.db.models.functions import Distance
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

        queryset = Tip.objects.all()

        if not (longitude and latitude):
            return queryset

        location = Point(longitude, latitude)
        close_cities = City.objects.filter(
                location__distance_lte=(location, D(km=10))).annotate(
                        distance=Distance('location', location))

        closest_city = close_cities.order_by('distance')[:1][0]

        queryset = queryset.filter(
                cities=closest_city,
                regions=closest_city.region,
                country=closest_city.region.country)

        return queryset

class TipperViewSet(viewsets.ModelViewSet):
    queryset = Tipper.objects.all()
    serializer_class = TipperSerializer
