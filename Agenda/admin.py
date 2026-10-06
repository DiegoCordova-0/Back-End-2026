from django.contrib import admin
from .models import Contacto

# Register your models here.

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'correo', 'direccion')
    search_fields = ('nombre', 'correo', 'telefono')
    list_filter = ('correo',)
    ordering = ('nombre',)
