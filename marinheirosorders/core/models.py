from django.db import models
import uuid

class Dish(models.Model):
    id = models.BigAutoField(primary_key=True)
    department = models.CharField(max_length=100)
    dish_name = models.CharField(max_length=100)

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_time = models.DateTimeField(auto_now_add=True)
    table_number = models.IntegerField()
    waiter = models.CharField(max_length=100)
    is_outside = models.BooleanField(default=False)
    order_note = models.TextField(blank=True)

class OrderDish(models.Model):
    order = models.ForeignKey(Order, related_name='order_dishes', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, related_name='order_dishes', on_delete=models.CASCADE)
    amount = models.FloatField(default=1)  # Campo para quantidade
    dish_note = models.TextField(null=True, blank=True)  # Campo para nota do prato
