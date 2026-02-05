from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    TIPO_USUARIO = (
    ('ALUNO', 'Aluno'),
    ('PROFESSOR', 'Professor'),
    ('ADMIN', 'Administrador'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO)

    def __str__(self):
        return f"{self.user.username}-{self.tipo}"


class Trabalho(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    arquivo = models.FileField(upload_to='trabalhos/')
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='trabalhos_usuario'
    )
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo