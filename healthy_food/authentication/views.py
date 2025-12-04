from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.generic import View

from . import forms as auth_forms
from food_selection import forms as food_forms


def logout_user(request):
    logout(request)
    messages.success(request, "Vous êtes déconnecté !")
    return redirect('food_selection:home')

class LoginPageView(View):
    template_name = 'authentication/login.html'
    login_form = auth_forms.LoginForm

    def get(self, request):
        form = self.login_form()
        context = {
            'search_form': food_forms.SearchNewFood(),
            'form': form,
            'message': messages,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.login_form(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, "Vous avez été Connecté avec Succès !")
                return redirect('food_selection:home')
        message = 'Login ou Mot de Passe Invalide.'
        context = {
            'search_form': food_forms.SearchNewFood(),
            'form': form,
            'message': messages,
        }
        return render(request, self.template_name, context)
