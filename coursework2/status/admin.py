from django.contrib import admin
from .models import *

# Register your models here.
class statusAdmin(admin.ModelAdmin):
    list_display = ['author', 'textUpdate','created_at']
    list_filter = ['author']
    search_fields = ['author']

admin.site.register(StatusList, statusAdmin)