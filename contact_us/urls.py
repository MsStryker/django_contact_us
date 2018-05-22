from django.conf.urls import url

from .views import ContactMessageFormView

urlpatterns = [
    url(r'^$', ContactMessageFormView.as_view(), name='contact')
]
