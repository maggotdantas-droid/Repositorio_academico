from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistroForm



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


from django.contrib.auth.models import User


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        tipo = request.POST.get('tipo')  # ALUNO, PROFESSOR ou ADMIN

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe!')
            return render(request, 'register.html')

        # Cria o usuário
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # ADMIN vira staff
        user.is_staff = True if tipo == 'ADMIN' else False
        user.save()

        # 🔑 Atualiza o perfil criado pelo signal
        perfil = user.perfil
        perfil.tipo = tipo
        perfil.save()

        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('/')

    return render(request, 'register.html')




from django.contrib.auth.decorators import login_required




@login_required
def dashboard(request):
    perfil = Perfil.objects.get(user=request.user)

    if perfil.tipo == 'ADMIN':
        trabalhos = Trabalho.objects.all()

    elif perfil.tipo == 'PROFESSOR':
        trabalhos = Trabalho.objects.all()

    else:  # ALUNO
        trabalhos = Trabalho.objects.filter(autor=request.user)

    return render(request, 'dashboard.html', {
        'perfil': perfil,
        'trabalhos': trabalhos
    })


def logout_view(request):
    logout(request)
    return redirect('/')



from django.contrib.auth.decorators import login_required

from .forms import TrabalhoForm


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
def editar_trabalho(request, trabalho_id):
    # Busca o trabalho pelo ID, garantindo que ele exista
    trabalho = get_object_or_404(Trabalho, id=trabalho_id)

    # Apenas o autor do trabalho pode editar
    if trabalho.autor != request.user:
        return redirect('dashboard')  # redireciona se não for o autor

    if request.method == 'POST':
        form = TrabalhoForm(request.POST, request.FILES, instance=trabalho)
        if form.is_valid():
            form.save()  # salva as alterações
            return redirect('dashboard')
    else:
        form = TrabalhoForm(instance=trabalho)  # preenche o form com os dados atuais

    return render(request, 'usuarios/editar_trabalho.html', {'form': form, 'trabalho': trabalho})


from django.contrib.auth.decorators import login_required


@login_required
def excluir_trabalho(request, trabalho_id):
    trabalho = get_object_or_404(Trabalho, id=trabalho_id)
    perfil = Perfil.objects.get(user=request.user)

    # Regra de permissão:
    # ADMIN pode excluir qualquer trabalho
    # AUTOR pode excluir apenas o próprio trabalho
    if perfil.tipo == 'ADMIN' or trabalho.autor == request.user:
        trabalho.delete()

    return redirect('dashboard')



from django.shortcuts import render, get_object_or_404, redirect
from .forms import ComentarioForm
from .models import Trabalho, Comentario
from django.contrib.auth.decorators import login_required


@login_required
def comentar_trabalho(request, trabalho_id):
    trabalho = get_object_or_404(Trabalho, id=trabalho_id)

    # Verifica se o professor já comentou
    comentario_existente = Comentario.objects.filter(
        trabalho=trabalho,
        professor=request.user
    ).first()

    if request.method == 'POST':
        if comentario_existente:
            # Já existe comentário, não faz nada e redireciona com mensagem
            messages.warning(request, "Você já comentou este trabalho.")
            return redirect('dashboard')
        else:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                novo_comentario = form.save(commit=False)
                novo_comentario.trabalho = trabalho
                novo_comentario.professor = request.user
                novo_comentario.save()
                messages.success(request, "Comentário enviado com sucesso!")
                return redirect('dashboard')
    else:
        # GET: apenas exibe o formulário se não houver comentário
        if comentario_existente:
            form = None
        else:
            form = ComentarioForm()

    return render(request, 'usuarios/comentar.html', {
        'trabalho': trabalho,
        'form': form
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Comentario, Perfil


@login_required
def excluir_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    # Verifica se o usuário é admin ou autor do comentário
    perfil = get_object_or_404(Perfil, user=request.user)
    if perfil.tipo == 'ADMIN' or comentario.professor == request.user:
        comentario.delete()
        messages.success(request, "Comentário excluído com sucesso.")
    else:
        messages.error(request, "Você não tem permissão para excluir este comentário.")

    return redirect('dashboard')
