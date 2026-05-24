from django.contrib import admin
from .models import Crop
@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display=['name','ph_min','ph_max','temp_min','temp_max']
    search_fields=['name']
