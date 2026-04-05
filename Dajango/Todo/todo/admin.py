from django.contrib import admin
from .models import Task


# Register your models here.

# when i want to customize the admin interface for a model, i can create a ModelAdmin class and register it with the model.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'created_at', 'updated_at')
    list_filter = ('completed', 'created_at', 'updated_at')
    search_fields = ('title',)

admin.site.register(Task , TaskAdmin)