from rest_framework import viewsets
from .models import Scheme
from .serializers import SchemeSerializer
class SchemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Scheme.objects.all()
    serializer_class=SchemeSerializer
