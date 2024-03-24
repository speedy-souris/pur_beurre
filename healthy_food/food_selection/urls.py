from django.urls import path
from food_selection import views

app_name = 'food_selection'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('recorded/', views.recorded, name='recorded'),
    path('profile/', views.profile, name='profile'),
    path('contact-us/', views.contact, name='contact'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
]
