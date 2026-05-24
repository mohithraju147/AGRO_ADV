from django.db import models
class Farmer(models.Model):
    name=models.CharField(max_length=100)
    mobile=models.CharField(max_length=15,unique=True)
    street=models.CharField(max_length=200,blank=True)
    area=models.CharField(max_length=100,blank=True)
    district=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.CharField(max_length=10,blank=True)
    farm_size=models.DecimalField(max_digits=8,decimal_places=2,default=1.0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return f"{self.name} ({self.district})"
    class Meta: ordering=['-created_at']
