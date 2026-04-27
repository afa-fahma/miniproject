from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=200,null=True, blank=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


# Order Model
class Order(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15,null=True, blank=True)
    total= models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.TextField(default="Not provided")
    payment_method = models.CharField(max_length=50, default="stripe")
    payment_status = models.CharField(max_length=50, default="Pending")
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


# Cart Model

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name
    
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
# Create your models here.








