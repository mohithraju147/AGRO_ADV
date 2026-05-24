from django.contrib import admin
from .models import Scheme
@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display=['title','state','category','budget_crore']
    list_filter=['state','category']
    search_fields=['title']
