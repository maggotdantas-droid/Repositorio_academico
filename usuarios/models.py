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



class Comentario(models.Model):
    trabalho = models.ForeignKey(Trabalho, on_delete=models.CASCADE, related_name='comentarios')
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('trabalho', 'professor')  # Garante 1 comentário por professor por trabalho

    def __str__(self):
        return f"Comentário de {self.professor.username} em {self.trabalho.titulo}"


