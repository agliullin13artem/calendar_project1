from django.contrib import admin
from .models import Event





@admin.register(Event)
class EventModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_at', 'period')
    search_fields = ('name',)
    list_filter = ('start_at', 'period')