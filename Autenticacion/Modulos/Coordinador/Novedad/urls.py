from django.urls import path
from django.contrib.auth.decorators import login_required
from Modulos.Coordinador.Novedad.views import Novedad_View

app_name = 'novedad'
urlpatterns = [
    # Se ocupa el name al momento de hacer las redirecciones
    path('inicio/', login_required(Novedad_View.as_view()), name='inicio'),
]