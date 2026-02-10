

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('enviar/', views.enviar_trabalho, name='enviar_trabalho'),
    path('trabalho/<int:id>/', views.trabalho_detail, name='trabalho_detail'),
    path('trabalho/<int:trabalho_id>/editar/', views.editar_trabalho, name='editar_trabalho'),
    path('trabalho/<int:trabalho_id>/excluir/', views.excluir_trabalho, name='excluir_trabalho'),
    path('logout/', views.logout_view, name='logout'),
    path('trabalho/<int:trabalho_id>/comentario/', views.comentar_trabalho, name='comentar_trabalho'),
    path('comentario/<int:comentario_id>/excluir/', views.excluir_comentario, name='excluir_comentario'),


]



