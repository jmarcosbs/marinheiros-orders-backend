from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .service.print import print_order  # Importando a função de impressão
from .service.telegram_notify import send_notification
from unidecode import unidecode

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Normalizando os dados do pedido antes de enviar para print_order
        normalized_data = {key: unidecode(value) if isinstance(value, str) else value for key, value in serializer.data.items()}
        # print_order(normalized_data)  # Chamada para a função de impressão
        send_notification(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
