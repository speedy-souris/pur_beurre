from django.conf import settings
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
        next_url = request.GET.get('next', '')
        context = {
            'search_form': food_forms.SearchNewFood(),
            'form': form,
            'next_url': next_url,
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
                messages.success(request, "Vous avez été connecté avec succès !")
                # Redirection recovery
                redirect_to = request.POST.get('next')
                if redirect_to:
                    return redirect(redirect_to)
                return redirect('food_selection:home')
            else:
                # Case: Valid form but incorrect password/unknown user
                messages.error(request, 'Identifiant ou mot de passe invalide.')
        else:
            # Case: Invalid form (empty fields, incorrect format)
            messages.error(request, 'Veuillez vérifier les champs du formulaire.')
        # If you've arrived here, it means that the login has failed.
        next_url = request.POST.get('next', '')
        context = {
            'search_form': food_forms.SearchNewFood(),
            'form': form,
            'next_url': next_url,
        }
        return render(request, self.template_name, context)

def signup_page(request):
    signup_form = auth_forms.SignupForm()
    if request.method == 'POST':
        signup_form = auth_forms.SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            messages.success(request, "Vous êtes Maintenant Inscrit !")
            return redirect(settings.LOGIN_REDIRECT_URL)
    context = {
        'search_form': food_forms.SearchNewFood(),
        'form': signup_form,
        'message': messages,
    }
    return render(request, 'authentication/signup.html', context)