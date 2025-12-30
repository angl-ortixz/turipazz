from django.contrib import admin
from .models import SitioTuristico

@admin.register(SitioTuristico)
class SitioTuristicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'precio', 'destacado')
    list_filter = ('destacado',)
    search_fields = ('nombre', 'ubicacion')
