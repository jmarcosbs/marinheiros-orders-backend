from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from .models import Order
from .serializers import OrderSerializer
from .service.print import print_order, is_printer_offline, PrinterOfflineException  # Importando a função de impressão
from .service.telegram_notify import send_notification
from unidecode import unidecode
import re

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

        # Normalizando os dados do pedido antes de enviar para print_order
        normalized_data = {}
        
        # Remove acentos de todas as strings no serializer
        for key, value in serializer.data.items():
            if isinstance(value, str):  # Verifica se o valor é uma string
                normalized_data[key] = unidecode(value)  # Aplica unidecode para remover acentos
            else:
                normalized_data[key] = value  # Mantém valores não-string inalterados
        
        try:
            print(f'Impressora offline? {is_printer_offline()}')
            print_order(normalized_data)  # Chamada para a função de impressão
            send_notification(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PrinterOfflineException as e:
            return Response({"detail": e.default_detail}, status=e.status_code)
        except APIException as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

