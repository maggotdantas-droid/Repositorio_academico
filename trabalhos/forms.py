from django import forms
from .models import Trabalho

class TrabalhoForm(forms.ModelForm):
    class Meta:
        model = Trabalho
        fields = ['titulo','descricao','arquivo']


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Trabalho
        fields = ['avaliacao'] # Aqui você pode incluir o texto do comentário também