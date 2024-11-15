from django.contrib.auth.decorators import login_required

from Modulos.Login.views import *

from django.urls import path

app_name = 'login'

urlpatterns = [
    
    
    path('',MainView.as_view(),name = 'index'),
    
    #Autenticación
    path('accounts/login/',Login.as_view(), name='login'),
    
    path('logout/',login_required(LogoutUsuario),name = 'logout'),
    
    path('registro/',RegistroView.as_view(), name = 'registro'),
    
    path('clave_olvidar',ForgetPassword.as_view(),name='olvidar_clave'),
    
    path('restablecer_clave/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='restablecer_clave'),
    
    path('cambiar_clave/',ChangePasswordFirstSession.as_view(), name = 'cambiar_clave'),
    
    # Lista de personal
    path('personal/', Usuario_view.as_view(), name = 'personal'),
    
    path('editar_personal/<int:pk>', Usuario_update.as_view(), name='editar_personal'),


    #Inactivar/activar rol - usuario
    path('inactivar_usuario/<int:pk>', InactivarActivarUsuarioView.as_view(), name='inactivar_usuario'),

    path('inactivar_rol/<int:pk>', InactivarActivarRolView.as_view(), name='inactivar_rol'),


    path('confirmar_inactivacion_usuario/<int:pk>/', ConfirmarAccionUsuarioView.as_view(), name='confirmar_accion_usuario'),
    
    

    # Rol
    path('listar_rol/', Rol_View.as_view(), name = 'listar_rol'),
    
    path('crear_rol/', Rol_Create.as_view(), name = 'crear_rol'),

    path('editar_rol/<int:pk>', Rol_Update.as_view(), name = 'editar_rol' ),

    #Página de prohibición 
    path('acceso_restringido/',Acceso_Restringido.as_view(), name = 'acceso_restringido')
]
    
    


