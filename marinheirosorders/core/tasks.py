from celery import shared_task
import time

@shared_task
def tarefa_exemplo():
    time.sleep(10)  # Simula uma tarefa de longa execução
    print("Tarefa concluída!")
    return "Resultado da tarefa"
