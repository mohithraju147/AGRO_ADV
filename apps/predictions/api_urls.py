from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets
from .models import Prediction
from .serializers import PredictionSerializer
class PredictionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Prediction.objects.all()
    serializer_class=PredictionSerializer
router=DefaultRouter()
router.register('predictions',PredictionViewSet)
urlpatterns=[path('',include(router.urls))]
