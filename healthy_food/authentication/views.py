from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from authentication.forms import LoginForm
from food_selection.forms import SearchNewFood


def logout_user(request):
    logout(request)
    return redirect('food_selection:home')

def login_page(request):
    login_form = LoginForm()
    message = ''
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            if user is not None:
                login(request,user)
                message = f'{user.username} connecté'
            else:
                message = 'Login ou mot de passe invalide'
    context ={
        'search_form': SearchNewFood(),
        'form': login_form,
        'message': message,
    }
    return render(request, 'authentication/login.html', context)
