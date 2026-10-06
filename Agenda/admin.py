from django.contrib import admin, messages
from .models import Contacto

admin.site.site_header = 'Agenda Personal'
admin.site.site_title = 'Agenda Personal'
admin.site.index_title = 'Administración de contactos'

# Register your models here.

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'correo', 'direccion')
    search_fields = ('nombre', 'correo', 'telefono')
    list_filter = ('correo',)
    ordering = ('nombre',)
    actions = ['limpiar_direccion']

    @admin.action(description='Limpiar dirección de los contactos seleccionados')
    def limpiar_direccion(self, request, queryset):
        updated = queryset.filter(direccion__isnull=True).update(direccion='Sin dirección')
        self.message_user(
            request,
            f'{updated} contacto(s) actualizados.',
            messages.SUCCESS,
        )
