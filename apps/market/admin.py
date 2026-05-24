from django.contrib import admin
from .models import MarketPrice
@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display=['crop_name','category','market','state','modal_price','demand']
    list_filter=['category','state','demand']
    search_fields=['crop_name','market']
