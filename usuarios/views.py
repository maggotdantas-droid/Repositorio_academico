from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


from .models import Perfil
from .forms import RegistroForm
from .services.trabalho_service import TrabalhoService


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard')
        else:
            return render(request, 'login.html', {'erro':'Usuário ou senha inválidos'})
    return render(request, 'login.html')

def register_view(request):

    if request.method == "POST":

        form =RegistroForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            Perfil.objects.create(
                user=user,
                tipo=form.cleaned_data['tipo']
            )

            return redirect('/')

    else:
        form = RegistroForm()

    return render(request, 'register.html', {'form': form})



@login_required
def dashboard(request):
    # Usuário logado
    user = request.user

    # Admin: vê todos os trabalhos
    if user.is_staff:
        trabalhos = Trabalho.objects.all()
        perfil = None  # admin não precisa de Perfil
    else:
        try:
            perfil = Perfil.objects.get(user=user)
        except Perfil.DoesNotExist:
            perfil = None
            trabalhos = []

        if perfil:
            if perfil.tipo == 'ALUNO':
                trabalhos = Trabalho.objects.filter(autor=user)
            elif perfil.tipo == 'PROFESSOR':
                trabalhos = Trabalho.objects.all()
            else:
                trabalhos = []
        else:
            trabalhos = []

    return render(request, 'dashboard.html', {
        'perfil': perfil,
        'trabalhos': trabalhos
    })



def logout_view(request):
    logout(request)
    return redirect('/')



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TrabalhoForm
from .models import Trabalho

@login_required
def enviar_trabalho(request):

    if request.method == 'POST':
        form = TrabalhoForm(request.POST, request.FILES)
        if form.is_valid():
            trabalho = form.save(commit=False)
            trabalho.autor = request.user  # garante que o autor seja o aluno
            trabalho.save()
            return redirect('dashboard')
    else:
        form = TrabalhoForm()

    return render(request, 'usuarios/enviar_trabalho.html', {'form': form})




@login_required
def trabalho_detail(request, id):
    trabalho = get_object_or_404(Trabalho, id=id)
    perfil = Perfil.objects.get(user=request.user)

    # Permissão: aluno só vê seus trabalhos
    if perfil.tipo == 'Aluno' and trabalho.autor != request.user:
        return redirect('dashboard')

    return render(request, 'usuarios/trabalho_detail.html', {
        'trabalho': trabalho,
        'perfil': perfil
    })


@login_required
def editar_trabalho(request, id):
    trabalho = get_object_or_404(Trabalho, id=id)
    perfil = Perfil.objects.get(user=request.user)

    # Somente autor ou admin podem editar
    if trabalho.autor != request.user and perfil.tipo != 'Admin':
        return redirect('dashboard')

    if request.method == 'POST':
        form = TrabalhoForm(request.POST, request.FILES, instance=trabalho)
        if form.is_valid():
            TrabalhoService.atualizar_trabalho(form, trabalho)
            return redirect('trabalho_detail', id=trabalho.id)
    else:
        form = TrabalhoForm(instance=trabalho)

    return render(request, 'usuarios/enviar_trabalho.html', {
        'form': form,
        'editar': True
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Trabalho

@login_required
def excluir_trabalho(request, trabalho_id):
    trabalho = get_object_or_404(Trabalho, id=trabalho_id)

    # Só autor (aluno) ou admin pode excluir
    if request.user == trabalho.autor or request.user.is_staff:
        trabalho.arquivo.delete()
        trabalho.delete()

    return redirect('dashboard')
