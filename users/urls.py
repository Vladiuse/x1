from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('reset-password-codes', views.ResetPasswordView, basename='resetuserpasswordcode')

app_name = 'users'

urlpatterns = [
    path('login/', views.SessionLoginView.as_view(), name='login'),
    path('logout/', views.SessionLogoutView.as_view(), name='logout'),
    path('sign-up/', views.CustomUserRegisterView.as_view(), name='sign_up'),
    path('change-password/', views.CustomUserChangePasswordView.as_view(), name='change_password'),
]

urlpatterns += router.urls