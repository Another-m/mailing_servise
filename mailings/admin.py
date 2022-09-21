from django.contrib import admin

from .models import Mailing, Client, Message



@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['id', 'time_start', 'time_end', 'text', 'tag', 'mob_operator', ]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'tag', 'timezone', ]

@admin.register(Message)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'sending_status', 'mailing', 'client', ]
