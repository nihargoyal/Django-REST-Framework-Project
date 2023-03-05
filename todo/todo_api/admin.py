from django.contrib import admin
from . models import ToDo

# Register your models here.

admin.site.register(ToDo)

class TodoAdmin(admin.ModelAdmin):
    list_display = ['priority', 'task', 'completed']
    ordering = ['priority']