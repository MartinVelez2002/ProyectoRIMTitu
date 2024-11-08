from django.contrib.auth.decorators import login_required

from Modulos.Login.views import *

from django.urls import path

app_name = 'login'

urlpatterns = [
    
    
    path('',MainView.as_view(),name = 'index'),
    
    path('accounts/login/',Login.as_view(), name='login'),
    
    path('logout/',login_required(LogoutUsuario),name = 'logout'),
    
    path('registro/',RegistroView.as_view(), name = 'registro'),
    
    path('personal/', Usuario_view.as_view(), name = 'personal'),

    path('editar_personal/<int:pk>', Usuario_update.as_view(), name='editar_personal'),
    
    path('clave_olvidar',ForgetPassword.as_view(),name='olvidar_clave'),
    
    path('restablecer_clave/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='restablecer_clave'),
    
    path('cambiar_clave/',ChangePasswordFirstSession.as_view(), name = 'cambiar_clave')
]


