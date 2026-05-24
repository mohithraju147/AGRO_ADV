from django.db import models
class Crop(models.Model):
    name=models.CharField(max_length=100)
    local_name=models.CharField(max_length=200,blank=True)
    soil_types=models.JSONField(default=list)
    ph_min=models.FloatField(default=5.5); ph_max=models.FloatField(default=7.5)
    temp_min=models.FloatField(default=20.0); temp_max=models.FloatField(default=35.0)
    rainfall_min=models.FloatField(default=500.0); rainfall_max=models.FloatField(default=1500.0)
    humidity_min=models.FloatField(default=40.0); humidity_max=models.FloatField(default=90.0)
    n_min=models.FloatField(default=20.0); n_max=models.FloatField(default=120.0)
    p_min=models.FloatField(default=20.0); p_max=models.FloatField(default=80.0)
    k_min=models.FloatField(default=20.0); k_max=models.FloatField(default=80.0)
    cultivation_steps=models.TextField(blank=True)
    water_needs=models.TextField(blank=True)
    disease_control=models.TextField(blank=True)
    suitable_regions=models.JSONField(default=list)
    crop_calendar=models.JSONField(default=dict)
    def __str__(self): return self.name
    class Meta: ordering=['name']
