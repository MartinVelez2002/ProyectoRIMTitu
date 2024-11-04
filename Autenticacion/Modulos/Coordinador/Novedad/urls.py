from django.urls import path
from django.contrib.auth.decorators import login_required
from Modulos.Coordinador.Novedad.views import Novedad_View, Novedad_Create, TipoNovedad_Create, TipoNovedad_View

app_name = 'novedad'
urlpatterns = [
    # Se ocupa el name al momento de hacer las redirecciones
    path('inicio/', login_required(Novedad_View.as_view()), name = 'inicio'),
    
    path('crear_novedad/', login_required(Novedad_Create.as_view()), name = 'crear_novedad'),
    
    path('crear_tipNov/', login_required(TipoNovedad_Create.as_view()), name = 'crear_tipNov'),
    
    path('inicio_tipoNov/', login_required(TipoNovedad_View.as_view()), name = 'inicio_tipoNov')
]