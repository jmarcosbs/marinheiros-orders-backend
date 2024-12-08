from __future__ import absolute_import, unicode_literals

# Sempre que o Django iniciar, carregue o Celery
from .celery import app as celery_app

__all__ = ('celery_app',)
