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
    dishes = models.ManyToManyField(Dish, related_name='dishes')
