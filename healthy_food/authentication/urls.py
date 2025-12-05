import authentication.views
from django.urls import path


app_name = 'authentication'
urlpatterns = [
    path('login/', authentication.views.LoginPageView.as_view(), name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
]
