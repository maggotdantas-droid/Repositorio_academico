from trabalhos.models import Trabalho
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from ..models import Trabalho

class TrabalhoService:
    @staticmethod
    def listar_trabalhos(usuario, perfil_tipo, busca=None):
        """
        Retorna trabalhos visíveis para o usuário.
        - Aluno: apenas seus próprios trabalhos
        - Professor/Admin: todos os trabalhos
        - busca: filtro opcional por título, autor ou data
        """
        # Garantir que tipo do perfil seja consistente
        perfil_tipo = perfil_tipo.lower()

        # Queryset base
        if perfil_tipo in ['professor', 'admin']:
            trabalhos = Trabalho.objects.all()
        else:
            trabalhos = Trabalho.objects.filter(autor=usuario)

        # Aplicar filtro se houver termo
        if busca:
            trabalhos = trabalhos.filter(
                Q(titulo__icontains=busca) |
                Q(autor__username__icontains=busca) |
                Q(data_envio__icontains=busca)  # funciona se data_envio for DateField ou CharField
            )

        return trabalhos.order_by('-data_envio')

    @staticmethod
    def excluir_trabalho(trabalho_id, usuario):
        try:
            trabalho = Trabalho.objects.get(id=trabalho_id)
        except Trabalho.DoesNotExist:
            return False

        # Regra de permissão:
        # aluno só pode excluir o próprio trabalho
        # professor pode excluir qualquer um
        if trabalho.autor != usuario and not usuario.is_staff:
            raise PermissionDenied("Você não tem permissão para excluir este trabalho.")

        trabalho.delete()
        return True
