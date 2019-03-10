from rest_framework import viewsets

from .models import Tip, Tipper
from .serializers import TipSerializer, TipperSerializer


class TipViewSet(viewsets.ModelViewSet):
    queryset = Tip.objects.all().order_by('-score')
    serializer_class = TipSerializer

class TipperViewSet(viewsets.ModelViewSet):
    queryset = Tipper.objects.all()
    serializer_class = TipperSerializer
