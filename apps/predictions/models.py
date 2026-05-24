from django.db import models
from apps.farmers.models import Farmer
class Prediction(models.Model):
    farmer=models.ForeignKey(Farmer,on_delete=models.CASCADE,related_name='predictions')
    soil_type=models.CharField(max_length=50)
    ph_value=models.FloatField()
    nitrogen=models.FloatField(default=60)
    phosphorus=models.FloatField(default=40)
    potassium=models.FloatField(default=40)
    temperature=models.FloatField(default=25)
    humidity=models.FloatField(default=65)
    rainfall=models.FloatField(default=800)
    crop_name=models.CharField(max_length=100)
    confidence=models.FloatField(default=0.85)
    top3_crops=models.JSONField(default=list)
    reason=models.TextField(blank=True)
    seed_cost=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    fertilizer=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    labour_cost=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    expected_rev=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    net_profit=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return f"{self.farmer.name} -> {self.crop_name}"
