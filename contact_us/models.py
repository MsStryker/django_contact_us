from __future__ import unicode_literals

from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.core import urlresolvers
from django.core.exceptions import ValidationError
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


MAX_MESSAGES_PER_IP = 2
MAX_MESSAGES_PER_DAY = 100


@python_2_unicode_compatible
class ContactSettings(models.Model):
    default = models.BooleanField(default=False, db_index=True)
    max_messages_per_day = models.PositiveIntegerField(default=MAX_MESSAGES_PER_DAY)
    max_messages_per_ip = models.PositiveIntegerField(default=MAX_MESSAGES_PER_IP,
                                                      help_text=_('Maximum number of messages per day per IP address.'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    timestamp = models.DateTimeField(auto_now=True)
    timestamp_uuid = models.UUIDField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Contact Message Settings'
        get_latest_by = 'timestamp'

    def __str__(self):
        return "{}/{}".format(self.max_messages_per_day, self.max_messages_per_ip)

    @classmethod
    def max_ip_count(cls):
        objs = cls.objects.filter(default=True)
        if objs.exists():
            return objs.latest().max_messages_per_ip
        return MAX_MESSAGES_PER_DAY

    @classmethod
    def max_count(cls):
        objs = cls.objects.filter(default=True)
        if objs.exists():
            return objs.latest().max_messages_per_day
        return MAX_MESSAGES_PER_DAY


@python_2_unicode_compatible
class ContactMessage(models.Model):
    TECHNICAL_ISSUES = 'TI'
    FEEDBACK = 'F'
    OTHER = 'O'
    SUBJECT_CHOICES = (
        ('', _('Select Your Subject')),
        (TECHNICAL_ISSUES, _('Technical Issues')),
        (FEEDBACK, _('Feedback')),
        (OTHER, _('Other'))
    )
    subject = models.CharField(max_length=3, choices=SUBJECT_CHOICES, db_index=True, blank=True, null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(db_index=True, blank=False)
    message = models.CharField(max_length=250, blank=False)
    ip_address = models.GenericIPAddressField(db_index=True)
    real_ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True, editable=False, db_index=True)
    read = models.BooleanField(default=False)
    read_timestamp = models.DateTimeField(auto_now=False, blank=True, null=True)
    last_read_timestamp = models.DateTimeField(auto_now=False, blank=True, null=True)
    mark_unread_timestamp = models.DateTimeField(auto_now=False, blank=True, null=True)

    starred = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Message Received'
        verbose_name_plural = 'Messages Received'

    def __str__(self):
        return "%s: %s" % (self.email, self.subject)

    @property
    def received(self):
        current_dt = timezone.now()
        diff_dt = current_dt - self.timestamp

        if diff_dt.days > 1:
            return '{} days ago'.format(diff_dt.days)
        elif diff_dt.days == 1:
            return 'Yesterday'
        else:
            minutes = diff_dt.seconds / 60
            hours = minutes / 60
            if hours < 1:
                if minutes < 2:
                    return 'A minute ago'
                return '{} minutes ago'.format(minutes)
            elif hours == 1:
                return 'An hour ago'
            else:
                return '{} hours ago'.format(hours)

    @classmethod
    def can_post(cls, ip_address=None):
        last_24 = timezone.now() - timedelta(days=1)
        objs = cls.objects.filter(timestamp__gte=last_24)
        if objs.count() >= ContactSettings.max_count():
            return False
        if not ip_address:
            return True

        objs = objs.filter(ip_address=ip_address)
        return objs.count() < ContactSettings.max_ip_count()

    @classmethod
    def mark_read(cls, object_id):
        obj = cls.objects.get(pk=object_id)
        obj.read = True
        if not obj.read_timestamp:
            obj.read_timestamp = timezone.now()
        obj.last_read_timestamp = timezone.now()
        obj.save(update_fields=['read_timestamp', 'read', 'last_read_timestamp'])

    @classmethod
    def get_read(cls):
        return cls.objects.filter(read=True).order_by('-timestamp')

    @classmethod
    def get_unread(cls):
        return cls.objects.filter(read=False).order_by('-timestamp')

    @classmethod
    def get_admin_messages(cls, max_display=3):
        return {'messages': cls.get_unread()[:max_display], 'read_all_link': cls.get_admin_messages_url()}

    def get_admin_url(self):
        return urlresolvers.reverse("admin:%s_%s_change" %
                                    (self._meta.app_label, self._meta.model_name), args=(self.pk,))

    @classmethod
    def get_admin_messages_url(cls):
        return urlresolvers.reverse("admin:%s_%s_changelist" % (cls._meta.app_label, cls._meta.model_name))

    @classmethod
    def is_duplicate(cls, obj):
        return cls.objects.filter(name=obj.name, subject=obj.subject, message=obj.message).exists()

    def clean(self):
        if self.is_duplicate(self):
            raise ValidationError(_('This appears to be a duplicate message submission?'))

        if not self.can_post(self.ip_address):
            raise ValidationError(_('Cannot accept any contacts at the moment, please try again later.'))

    def save(self, *args, **kwargs):
        if self.read_timestamp:
            self.read = True

        super(ContactMessage, self).save(*args, **kwargs)
