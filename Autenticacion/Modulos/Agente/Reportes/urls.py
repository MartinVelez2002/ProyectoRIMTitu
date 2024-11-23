from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'reportes'
urlpatterns =[
    path('listar_reportes/', Reportes_View.as_view(), name = 'listar_reportes'),

    path('crear_reporte/', IncidenteCreateView.as_view(), name = 'crear_reporte'),

    # path('adicionar_detalle/<int:pk>/', AdicionarDetalle.as_view(), name = 'adicionar_detalle'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)