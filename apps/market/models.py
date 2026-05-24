from django.db import models
class MarketPrice(models.Model):
    CATS=[('grain','Grain'),('vegetable','Vegetable'),('fruit','Fruit')]
    crop_name=models.CharField(max_length=100)
    category=models.CharField(max_length=20,choices=CATS,default='grain')
    state=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    market=models.CharField(max_length=100)
    min_price=models.DecimalField(max_digits=10,decimal_places=2)
    max_price=models.DecimalField(max_digits=10,decimal_places=2)
    modal_price=models.DecimalField(max_digits=10,decimal_places=2)
    demand=models.CharField(max_length=20,default='moderate')
    recorded_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['crop_name']
    def __str__(self): return f"{self.crop_name}-{self.market}-Rs.{self.modal_price}"
