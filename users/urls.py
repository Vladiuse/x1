from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.SessionLoginView.as_view(), name='login'),
    path('logout/', views.SessionLogoutView.as_view(), name='logout'),
    path('sign-up/', views.CustomUserRegisterView.as_view(), name='sign_up'),
]