from django.contrib import admin
from .models import PlantInfo

@admin.register(PlantInfo)
class PlantInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'prediction', 'image', 'created_at')
    search_fields = ('user__email', 'prediction')
    list_filter = ('created_at',)
