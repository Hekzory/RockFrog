from django.contrib import admin

from .models import *


class ConversationsListAdmin(admin.ModelAdmin):
    fields = ['user', 'conversations']


admin.site.register(ConversationList, ConversationsListAdmin)


class ConversationAdmin(admin.ModelAdmin):
    fields = ['user1', 'user2', 'messages', 'last_interaction', 'last_view_user1', 'last_view_user2']


admin.site.register(Conversation, ConversationAdmin)


class ConversationMessageAdmin(admin.ModelAdmin):
    fields = ['user', 'text', 'date_time']


admin.site.register(ConversationMessage, ConversationMessageAdmin)
