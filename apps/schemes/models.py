from django.db import models
class Scheme(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    ministry=models.CharField(max_length=200,blank=True)
    state=models.CharField(max_length=100,blank=True)
    benefit=models.TextField()
    eligibility=models.TextField(blank=True)
    apply_link=models.URLField(blank=True)
    budget_crore=models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    category=models.CharField(max_length=100,blank=True)
    def __str__(self): return self.title
    class Meta: ordering=['title']
