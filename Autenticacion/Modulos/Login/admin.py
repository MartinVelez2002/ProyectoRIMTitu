from django.contrib import admin
from .models import Usuario, Rol


admin.site.register(Rol)
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'nombre', 'apellido', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'nombre', 'apellido')