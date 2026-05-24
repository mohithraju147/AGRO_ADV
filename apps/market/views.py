from rest_framework import viewsets
from .models import MarketPrice
from .serializers import MarketPriceSerializer
class MarketPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=MarketPrice.objects.all()
    serializer_class=MarketPriceSerializer
