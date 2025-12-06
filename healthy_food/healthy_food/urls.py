# url.py of the main project
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('food/', include('food_selection.urls')),
    path('auth/', include('authentication.urls')),
    path('', RedirectView.as_view(url='food/', permanent=False)),
]
