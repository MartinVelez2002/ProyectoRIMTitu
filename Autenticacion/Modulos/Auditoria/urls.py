from django.urls import path
from .views import Auditoria_View 

app_name = 'auditoria'

urlpatterns = [
    path('listar_auditoria/', Auditoria_View.as_view(), name = 'listar_auditoria')
]