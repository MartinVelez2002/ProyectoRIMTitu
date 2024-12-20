"""ecommerse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the-include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls.static import static
from Auth import settings
from django.contrib import admin





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Modulos.Login.urls')),
    path('novedad/', include('Modulos.Coordinador.Novedad.urls')),
    path('ubicacion/', include('Modulos.Coordinador.Ubicacion.urls')),
    path('turno/', include('Modulos.Coordinador.Turno.urls')),
    path('calendario/', include('Modulos.Coordinador.Calendario.urls')),
    path('auditoria/', include('Modulos.Auditoria.urls')),
    path('reportes/', include('Modulos.Agente.Reportes.urls')),
    path('reportesCoord/', include('Modulos.Coordinador.List_Reportes.urls')),
]   

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

