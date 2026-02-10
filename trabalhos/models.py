from django.db import models
from django.contrib.auth.models import User

class Trabalho(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    arquivo = models.FileField(upload_to='trabalhos/')
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='trabalhos'
    )
    data_envio = models.DateTimeField(auto_now_add=True)
    nota_professor = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self):
        return self.titulo
