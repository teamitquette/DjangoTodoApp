from django.contrib import admin
from .models import TodoItem

# Register your models here for admin panel
@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'completed', 'created_at']
    list_filter = ['completed', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
