from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from authentication.forms import LoginForm
from food_selection.forms import SearchNewFood


def logout_user(request):
    logout(request)
    messages.success(request, "Vous êtes déconnecté !")
    return redirect('food_selection:home')

def login_page(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            if user is not None:
                login(request,user)
                messages.success(request, "Vous avez été connecté avec succès !")
                return redirect('food_selection:home')
            else:
                messages.error(request, "Login ou mot de passe invalide")
    context ={
        'search_form': SearchNewFood(),
        'form': login_form,
        'message': messages,
    }
    return render(request, 'authentication/login.html', context)
