# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite
from django_summernote.admin import SummernoteModelAdmin, SummernoteWidget
from .models import sb_mail_server, mail_server, sbmail_template, Email_Subscription, mail_message, \
    mail_message_attachment, sb_settings


# Register your models here.

class sbmail_templateAdminForm(forms.ModelForm):
    class Meta:
        model = sbmail_template
        widgets = {
            'body_html': SummernoteWidget(),
            'body_text': SummernoteWidget(),
        }
        fields = '__all__'


class mail_messageAdminForm(forms.ModelForm):
    class Meta:
        model = mail_message
        widgets = {
            'body_text': SummernoteWidget(),
            'body_html': SummernoteWidget(),
        }
        fields = '__all__'


class sb_settingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'support_email')
    list_filter = ('signup_group', 'support_email')
    search_fields = ('signup_group', 'support_email')


class sb_mail_serverAdmin(admin.ModelAdmin):
    list_display = ('name', 'server', 'type', 'state', 'server_type', 'priority')
    # readonly_fields = ('priority','type')
    list_filter = ('name', 'server', 'type', 'state', 'server_type', 'priority')
    search_fields = ('name', 'server', 'type', 'state', 'server_type', 'priority')


class sbmail_templateAdmin(admin.ModelAdmin):
    form = sbmail_templateAdminForm
    list_display = ('name', 'type')
    # readonly_fields = ('name','type')
    list_filter = ('name', 'type')
    search_fields = ('name', 'type')


class Email_SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'active')
    # readonly_fields = ('email','active')
    list_filter = ('name', 'email', 'active')
    search_fields = ('name', 'email', 'active')


class mail_messageAdmin(admin.ModelAdmin):
    form = mail_messageAdminForm
    list_display = ('subject', 'to_email', 'from_email', 'status')
    # readonly_fields = ('bbc_email','cc_email')
    list_filter = ('subject', 'to_email', 'from_email', 'status')
    search_fields = ('subject', 'to_email', 'from_email', 'status')


class mail_message_attachmentAdmin(admin.ModelAdmin):
    list_display = ('mail_message_id', 'title', 'time')
    # readonly_fields = ('title','time')
    list_filter = ('mail_message_id', 'title', 'time')
    search_fields = ('mail_message_id', 'title', 'time')


# PURPOSE:
class MyPostAdmin(sb_mail_serverAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(type="In")


class mail_serverAdmin(sb_mail_serverAdmin):
    readonly_fields = ('priority', 'type')
    list_filter = ('name', 'server', 'type', 'state', 'server_type')
    search_fields = ('name', 'server', 'type', 'state', 'server_type')

    def get_queryset(self, request):
        return self.model.objects.filter(type="Out")


admin.site.register(sb_settings, sb_settingsAdmin)
admin.site.register(mail_message_attachment, mail_message_attachmentAdmin)
admin.site.register(mail_message, mail_messageAdmin)
admin.site.register(sb_mail_server, MyPostAdmin)
admin.site.register(mail_server, mail_serverAdmin)
admin.site.register(sbmail_template, sbmail_templateAdmin)
admin.site.register(Email_Subscription, Email_SubscriptionAdmin)
