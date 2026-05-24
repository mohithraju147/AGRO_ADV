from django.contrib import admin
from .models import Prediction
@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display=['farmer','crop_name','confidence','soil_type','ph_value','net_profit','created_at']
    list_filter=['crop_name','soil_type']
    search_fields=['farmer__name','crop_name']
    readonly_fields=['created_at']
