from django.contrib import admin
from django.contrib.auth.decorators import login_required

from Modulos.Login.views import *

from django.urls import path

app_name = 'login'

urlpatterns = [
    path('admin/', login_required(AdminRedirectView.as_view()), name='admin'),
    
    path('',MainView.as_view(),name = 'index'),
    
    path('accounts/login/',Login.as_view(), name='login'),
    
    path('logout/',login_required(LogoutUsuario),name = 'logout'),
    
    path('registro/',RegistroView.as_view(), name = 'registro'),
    
    path('personal/', Usuario_view.as_view(), name = 'personal'),
    
    path('clave_olvidar',ForgetPassword.as_view(),name='olvidar_clave'),
    
    path('restablecer_clave/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='restablecer_clave'),
    
    path('cambiar_clave/',ChangePasswordFirstSession.as_view(), name = 'cambiar_clave')
]


