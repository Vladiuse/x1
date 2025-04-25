from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.SessionLoginView.as_view(), name='login'),
]