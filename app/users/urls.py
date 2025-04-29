from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('reset-password-codes', views.ResetPasswordView)

app_name = 'users'

urlpatterns = [
    path('login/', views.SessionLoginView.as_view(), name='login'),
    path('logout/', views.SessionLogoutView.as_view(), name='logout'),
    path('sign-up/', views.CustomUserRegisterView.as_view(), name='sign_up'),
    path('change-password/', views.CustomUserChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('deactivate-reset-code/<int:reset_code_id>/', views.deactivate_reset_code, name='deactivate_reset_code'),
]

urlpatterns += router.urls
