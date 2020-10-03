from django.contrib import admin

# Register your models here.
from .models import Profile, PrivacySettings, NotificationSettings, NewsFeedSettings


class ProfilesAdmin(admin.ModelAdmin):
    fields = ['user', 'about', 'birth_date', 'avatar', 'blacklist', 'verified', 'last_time_online']
    readonly_fields = ['user']
    empty_value_display = 'Не указано'

class PrivacySettingsAdmin(admin.ModelAdmin):
    fields = ['allow_to_view_for_unreg', 'profile']

class NewsFeedSettingsAdmin(admin.ModelAdmin):
    fields = ['defaultsection', 'showviewed', 'profile']

class NotificationSettingsAdmin(admin.ModelAdmin):
    fields = ['personal_message_notifications', 'accepted_to_group_notifications', 'post_published_notifications',
              'profile']


admin.site.register(Profile, ProfilesAdmin)
admin.site.register(PrivacySettings, PrivacySettingsAdmin)
admin.site.register(NewsFeedSettings, NewsFeedSettingsAdmin)
admin.site.register(NotificationSettings, NotificationSettingsAdmin)