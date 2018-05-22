from datetime import timedelta

from freezegun import freeze_time

from django.test import TestCase
from django.utils import timezone

from contact_us.models import ContactMessage

from tests.factories import ContactMessageFactory, ContactSettingsFactory


class ContactMessageTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.timestamp = timezone.now()
        super(ContactMessageTestCase, cls).setUpClass()
        for i in range(5):
            with freeze_time(cls.timestamp - timedelta(days=i)):
                obj = ContactMessageFactory()
                obj.save()

        for i in range(3):
            with freeze_time(cls.timestamp - timedelta(hours=i+1)):
                obj = ContactMessageFactory(read_timestamp=cls.timestamp)
                obj.save()

    @classmethod
    def tearDown(cls):
        ContactMessage.objects.all().delete()

    def test_get_unread(self):
        objs = ContactMessage.get_unread()
        self.assertEqual(objs.count(), 5)
        self.assertEqual(objs[0].timestamp, self.timestamp)

    def test_read(self):
        objs = ContactMessage.get_read()
        self.assertEqual(objs.count(), 3)
        self.assertEqual(objs[0].read_timestamp, self.timestamp)

    def test_can_post_true(self):
        self.assertTrue(ContactMessage.can_post())

    def test_can_post_false(self):
        obj = ContactSettingsFactory.create(default=True, max_messages_per_day=1)
        self.assertFalse(ContactMessage.can_post())

    def test_is_duplicate_true(self):
        existing_obj = ContactMessage.objects.all()[0]
        obj = ContactMessageFactory.build(name=existing_obj.name,
                                          subject=existing_obj.subject,
                                          message=existing_obj.message)
        self.assertTrue(ContactMessage.is_duplicate(obj))

    def test_is_duplicate_false(self):
        existing_obj = ContactMessage.objects.all()[0]
        obj = ContactMessageFactory.build(name='New Name',
                                          subject=existing_obj.subject,
                                          message=existing_obj.message)
        self.assertFalse(ContactMessage.is_duplicate(obj))
