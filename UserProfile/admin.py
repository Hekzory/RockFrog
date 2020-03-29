from django.contrib import admin

# Register your models here.
from .models import Profile, PrivacySettings

class ProfilesAdmin(admin.ModelAdmin):
    fields = ['user', 'about', 'birth_date', 'avatar']
    readonly_fields = ['user']
    empty_value_display = 'Не указано'

class PrivacySettingsAdmin(admin.ModelAdmin):
    fields = ['allow_to_view_for_unreg', 'profile']


admin.site.register(Profile, ProfilesAdmin)
admin.site.register(PrivacySettings, PrivacySettingsAdmin)