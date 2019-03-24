from django.contrib.gis.geos import Point 
from cities.models import City
from rest_framework import viewsets

from .models import Tip, Tipper
from .serializers import TipSerializer, TipperSerializer


class TipViewSet(viewsets.ModelViewSet):
    queryset = Tip.objects.all().order_by('-score')
    serializer_class = TipSerializer

    def get_queryset(self):
        longitude = self.request.query_params.get('longitude')
        latitude= self.request.query_params.get('latitude')

        location = Point(longitude, latitude)
        closest_city = City.objects.distance(location).order_by('distance')[:1]

        queryset = Model.object.filter(cities=closest_city)

class TipperViewSet(viewsets.ModelViewSet):
    queryset = Tipper.objects.all()
    serializer_class = TipperSerializer
