from django.urls import path
from .views import enviar_trabalho

urlpatterns = [
    path('enviar/', enviar_trabalho,
    name ='enviar_trabalho'),
]