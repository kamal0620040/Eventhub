from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):
    """List Admin Model"""
    
    list_display = ("name","user","count_event",)
    search_fields = ("name",)