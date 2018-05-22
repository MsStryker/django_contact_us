from django.contrib import admin
from django.contrib.admin import register

from .models import ContactMessage, ContactSettings


@register(ContactSettings)
class ContactSettingsAdmin(admin.ModelAdmin):
    list_display = ('max_messages_per_day', 'max_messages_per_ip', 'timestamp', 'default', 'timestamp_uuid')
    list_filter = ('default',)
    readonly_fields = ('timestamp_uuid',)
    save_as = True

    def save_model(self, request, obj, form, change):
        obj.timestamp__uuid = request.user.uuid
        obj.save()


@register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'read', 'email', 'starred', 'timestamp', 'name', 'message', 'ip_address')
    list_filter = ('subject', 'read', 'starred')
    list_editable = ('starred',)
    search_fields = ('email', 'name', 'subject', 'ip_address')
    readonly_fields = (
        'name',
        'email',
        'subject',
        'message',
        'ip_address',
        'real_ip_address',
        'timestamp',
        'read_timestamp',
        'last_read_timestamp',
        'mark_unread_timestamp')

    fields = (
        ('read', 'starred'),
        ('name', 'email', 'timestamp'),
        'subject', 'message',
        ('ip_address', 'real_ip_address'),
        'read_timestamp'
    )

    def has_add_permission(self, request):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if object_id:
            ContactMessage.mark_read(object_id)

        if extra_context is None:
            extra_context = {}

        extra_context['show_save'] = False
        extra_context['show_save_as_new'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False

        return super(ContactMessageAdmin, self).changeform_view(request, object_id=object_id, form_url=form_url,
                                                                extra_context=extra_context)

