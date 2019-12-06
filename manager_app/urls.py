from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('<str:something>/new/', views.something_new, name = 'something_new'),
    path('<str:something>/view/', views.view_something, name = 'view_something'),
    path('accounts/profile/clear/', views.clear_figures, name='clear_figures'),
]