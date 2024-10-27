from datetime import datetime
from win32 import win32print

# dish_name da impressora (substitua com o dish_name da sua impressora ESC/P)
print_name = win32print.GetDefaultPrinter()


def print_order(order_data):
    print(order_data)
    
    # Agora você pode acessar os dados do pedido
    order_id = order_data['id']
    
    original_date_time = order_data['date_time']
    # Converter a string para um objeto datetime
    date_object = datetime.fromisoformat(original_date_time[:-2] + "00")  # Remove o 'Z' no final
    # Formatar a data no formato desejado
    date_time = date_object.strftime("%d-%m-%Y %H:%M:%S")

    table_number = order_data['table_number']
    order_dishes = order_data['order_dishes']
    order_note = order_data['order_note']
    waiter = order_data['waiter']
    is_outside = order_data['is_outside']
    
    # Abra a impressora para se comunicar diretamente
    hPrinter = win32print.OpenPrinter(print_name)
    hJob = win32print.StartDocPrinter(hPrinter, 1, (f'pedido_{order_id}_mesa_{table_number}', None, "RAW"))
    win32print.StartPagePrinter(hPrinter)
    
    # Enviar os comandos para a impressora
    win32print.WritePrinter(hPrinter, cabecalho_pedido(order_id, date_time, waiter))
    imprimir_cozinha(hPrinter, order_dishes)
    win32print.WritePrinter(hPrinter, rodape_pedido(order_note, table_number, is_outside))

    # Finalizar o trabalho de impressão
    win32print.EndPagePrinter(hPrinter)
    win32print.EndDocPrinter(hPrinter)
    win32print.ClosePrinter(hPrinter)



def cabecalho_pedido(order_id, data_time, waiter):
    comandos = (
        b'\x1B\x40'  # Resetar a impressora (ESC @)
        b'\x1B\x61\x01'  # Centralizar texto (ESC a 1)
        b'\x1B\x21\x20'  # Fonte média
        +
        format_text(f'#Pedido {order_id}\n', 'medium').encode('utf-8')
        +
        b'\x1B\x61\x00'  # Alinhar à esquerda (ESC a 0)
        b'\x1B\x21\x00'  # Fonte pequena (ESC ! 0)
        +
        format_text(f'Data: {data_time}\n', 'small').encode('utf-8')
        +
        format_text(f'Atendente: {waiter}\n\n\n', 'small').encode('utf-8')
    )
    return comandos

def dishes_pedido(dish_name, amount, dish_note):
    comandos = (
        b'\x1B\x21\x30'  # Fonte muito grande (ESC ! 48)
        b'\x1B\x45\x01'  # Ativar negrito (ESC E 1)
        +
        format_text(f'{amount}x {dish_name}\n\n', 'big').encode('utf-8')
        +
        b'\x1B\x45\x00'  # Desativar negrito (ESC E 0)
        b'\x1B\x21\x20'  # Fonte média
        +
        format_text(f'    {dish_note}\n\n', 'medium').encode('utf-8')
    )
    return comandos

def rodape_pedido(order_note, table_number, is_outside):
    comandos = (
        format_text(f'\n{order_note}\n\n', 'medium').encode('utf-8')
        +
        b'\x1B\x61\x01'  # Centralizar texto (ESC a 1)
        b'\x1B\x45\x01'  # Ativar negrito (ESC E 1)
        b'\x1B\x2D\x01'  # Ativa sublinhado
        b'\x1B\x21\x30'  # Fonte muito grande (ESC ! 48)
        +
        format_text(f"* Mesa {'R' + str(table_number) if is_outside else str(table_number)} *\n\n\n", 'big').encode('utf-8')
        +
        b'\x1B\x2D\x00'  # Desativa sublinhado
        b'\x1B\x45\x00'  # Desativar negrito (ESC E 0)
        b'\x1B\x61\x00'  # Alinhar à esquerda (ESC a 0)
    )
    return comandos


def imprimir_cozinha(hPrinter, order_dishes):
    for order_dish in order_dishes:
        dish = order_dish['dish']
        amount = order_dish['amount']
        dish_note = order_dish['dish_note']
        if dish['department'] == 'cozinha':
            # Enviar o comando para cada dish da cozinha
            dish_name = dish['dish_name']
            win32print.WritePrinter(hPrinter, dishes_pedido(dish_name, amount, dish_note))

# Exemplo de uso:
# texto_big = formatar_texto("Este é um texto de exemplo para testar a formatação.", 'big')
# texto_medium = formatar_texto("Este é um texto de exemplo para testar a formatação.", 'medium')
# texto_small = formatar_texto("Este é um texto de exemplo para testar a formatação.", 'small')

def format_text(text, other):
        return text

