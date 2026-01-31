from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Head(models.Model):
    animal = models.CharField(max_length=64)
    price_per_kilo = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    age = models.IntegerField()
    ready_for_sale = models.BooleanField(default=False)
    

    def __str__(self):
        return f'Animal: {self.animal}, Weight: {self.weight}, Age: {self.age}, $/kg: {self.price_per_kilo}, Ready for sale: {self.ready_for_sale}'

def add_30_days():
    return timezone.now() + timedelta(days=30)
class Order(models.Model):
    animal = models.CharField(max_length=64)
    animal_id = models.IntegerField(unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateField(auto_now_add=True)
    expected_arrival_date = models.DateField(default=add_30_days)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Animal: {self.animal}, Animal ID: {self.animal_id}, Total Price: {self.total_price}, Order Date: {self.order_date}, Expected to arrive at: {self.expected_arrival_date}'