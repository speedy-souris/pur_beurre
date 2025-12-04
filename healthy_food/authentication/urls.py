import authentication.views
from django.urls import path


app_name = 'authentication'
urlpatterns = [
    path('login/', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
]
