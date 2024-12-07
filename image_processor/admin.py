from django.contrib import admin
from .models import Detection

@admin.register(Detection)
class DetectionAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'object_name', 'object_count')
