
from django import forms
from .models import Trabalho


class RegistroForm(forms.Form):
    username = forms.CharField(label="Usuário")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    tipo = forms.ChoiceField(choices=[
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('ADMIN', 'Administrador'),
    ])

class TrabalhoForm(forms.ModelForm):
    class Meta:
        model = Trabalho
        fields = ['titulo','descricao','arquivo']



from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Digite seu comentário'
            })
        }
