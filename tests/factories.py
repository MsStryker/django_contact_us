from factory.django import DjangoModelFactory
from factory import LazyAttribute, Sequence

from contact_us.models import ContactMessage, ContactSettings


class ContactSettingsFactory(DjangoModelFactory):

    class Meta:
        model = ContactSettings

    default = True


class ContactMessageFactory(DjangoModelFactory):

    class Meta:
        model = ContactMessage

    subject = ContactMessage.OTHER
    name = 'Jane Doe'
    email = LazyAttribute(lambda obj: '%s@example.com' % obj.name.replace(' ', ''))
    message = Sequence(lambda n: 'Test message %d' % n)
    ip_address = '127.0.0.1'
