from rest_framework import serializers
from .models import Order, Dish, OrderDish

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'department', 'dish_name']

class OrderDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDish
        fields = ['dish', 'amount', 'dish_note']  # Campos do OrderDish

class OrderSerializer(serializers.ModelSerializer):
    order_dishes = OrderDishSerializer(many=True, write_only=True)  # Usando o novo serializer

    class Meta:
        model = Order
        fields = ['id', 'date_time', 'table_number', 'waiter', 'is_outside', 'order_note', 'order_dishes']

    def create(self, validated_data):
        order_dishes_data = validated_data.pop('order_dishes')
        order = Order.objects.create(**validated_data)
        for order_dish_data in order_dishes_data:
            OrderDish.objects.create(order=order, **order_dish_data)
        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['order_dishes'] = OrderDishSerializer(instance.order_dishes.all(), many=True).data
        return representation
