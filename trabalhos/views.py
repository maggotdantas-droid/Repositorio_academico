from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TrabalhoForm

@login_required
def enviar_trabalho(request):
    if request.method == 'POST':
        form = TrabalhoForm(request.POST, request.FILES)
        if form.is_valid():
            trabalho = form.save(commit=False)
            trabalho.autor = request.user
            trabalho.save()
            return redirect('dashboard')
    else:
        form = TrabalhoForm()
    return render(request, 'trabalhos/enviar_trabalho.html', {'form': form})

# Create your views here.
