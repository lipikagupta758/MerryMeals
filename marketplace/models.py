from django.db import models
from accounts.models import User
from vendor.models import FoodItem, Vendor

# Create your models here.

class Restaurant_Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    foodItem= models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=  models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user
    
class Cart(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=  models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user


