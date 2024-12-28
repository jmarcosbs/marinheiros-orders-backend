from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from threading import Thread
from .models import Order
from .serializers import OrderSerializer
from .service.print_kitchen import print_order_kitchen, is_printer_offline_kitchen, PrinterOfflineException  # Importando a função de impressão
from .service.print_all import print_order_all, is_printer_offline_all, PrinterOfflineException  # Importando a função de impressão
from .service.telegram_notify import send_notification
# Dentro de views.py
from .service.telegram_notify_kitchen import send_notification_kitchen
from unidecode import unidecode

class PrinterErrorException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Ocorreu um erro na impressora ao tentar processar o pedido."
    default_code = "printer_error"

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        def send_notifications(serializer_data):
            send_notification(serializer_data)
            send_notification_kitchen(serializer_data)

        # Normalizando os dados do pedido antes de enviar para print_order
        normalized_data = {}
        
        # Remove acentos de todas as strings no serializer
        for key, value in serializer.data.items():
            if isinstance(value, str):  # Verifica se o valor é uma string
                normalized_data[key] = unidecode(value)  # Aplica unidecode para remover acentos
            else:
                normalized_data[key] = value  # Mantém valores não-string inalterados
        
        try:
            print(f'Impressora offline cozinha? {is_printer_offline_kitchen()}')
            print(f'Impressora offline copa? {is_printer_offline_all()}')
            print_order_all(normalized_data)
            print_order_kitchen(normalized_data) # Chamada para a função de impressão
            background_thread = Thread(
                target=send_notifications, args=(serializer.data,)
            )
            background_thread.start()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PrinterOfflineException as e:
            return Response({"detail": e.default_detail}, status=e.status_code)
        except APIException as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

