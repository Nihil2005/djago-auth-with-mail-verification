# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_registration, name='user_registration'),
    path('confirm/', views.code_confirm, name='confirm'),
    path('home/', views.home, name='home'),

    # other paths...
]
