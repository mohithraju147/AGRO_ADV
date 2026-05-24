from rest_framework import serializers
from .models import Prediction
class PredictionSerializer(serializers.ModelSerializer):
    farmer_name=serializers.CharField(source='farmer.name',read_only=True)
    class Meta:
        model=Prediction; fields='__all__'
