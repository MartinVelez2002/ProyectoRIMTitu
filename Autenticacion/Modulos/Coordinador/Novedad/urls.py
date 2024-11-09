from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import Novedad_View, Novedad_Create, TipoNovedad_Create, TipoNovedad_View, TipoNovedad_Update, Novedad_Update

app_name = 'novedad'
urlpatterns = [
    # Se ocupa el name al momento de hacer las redirecciones
    # URLs de Novedad
    path('inicio/', Novedad_View.as_view(), name = 'inicio'),
    
    path('crear_novedad/', Novedad_Create.as_view(), name = 'crear_novedad'),
    
    path('editar_nov/<int:pk>', Novedad_Update.as_view(), name = 'editar_nov'),

    # URLs de TipoNovedad
    path('inicio_tipoNov/', TipoNovedad_View.as_view(), name = 'inicio_tipoNov'),
    
    path('crear_tipNov/', TipoNovedad_Create.as_view(), name = 'crear_tipNov'),
    
    path('editar_tipNov/<int:pk>', TipoNovedad_Update.as_view(), name = 'editar_tipNov'),
    
]