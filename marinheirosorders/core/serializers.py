from rest_framework import serializers
from .models import Order, Dish

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'department', 'dish_name']

class OrderSerializer(serializers.ModelSerializer):
    # Durante a criação do pedido, os pratos são enviados como uma lista de IDs
    dishes = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), many=True, write_only=True)
    
    # Na resposta, serialize os pratos completos
    dishes_details = DishSerializer(source='dishes', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'date_time', 'table_number', 'waiter', 'is_outside', 'order_note', 'dishes', 'dishes_details']

    def to_representation(self, instance):
        # Usa o método padrão para serializar os dados
        representation = super().to_representation(instance)
        # Remove o campo "dishes" da resposta (pois ele só contém os IDs)
        representation.pop('dishes', None)
        return representation
