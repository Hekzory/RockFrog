from django.contrib import admin

# Register your models here.
from .models import Profile

class ProfilesAdmin(admin.ModelAdmin):
    fields = ['user', 'about', 'birth_date']
    readonly_fields = ['user']
    empty_value_display = 'Не указано'

admin.site.register(Profile, ProfilesAdmin)
