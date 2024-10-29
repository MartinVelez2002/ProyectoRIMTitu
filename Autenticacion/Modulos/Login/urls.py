from django.contrib import admin
from django.contrib.auth.decorators import login_required

from Modulos.Login.views import Login,LogoutUsuario,MainView,RegistroView,ForgetPassword, PasswordResetConfirmView
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',MainView.as_view(),name = 'index'),
    path('accounts/login/',Login.as_view(), name='login'),
    path('logout',login_required(LogoutUsuario),name = 'logout'),
    path('registro',RegistroView.as_view(),name = 'registro'),
    path('clave_olvidar/',ForgetPassword.as_view(),name='olvidar_clave'),
    path('restablecer_clave/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='restablecer_clave'),

]