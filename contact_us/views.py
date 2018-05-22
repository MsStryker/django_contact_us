from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseRedirect

from .config import PAGE_CONTEXT
from .models import ContactMessage
from .forms import ContactMessageForm
from .utils import get_ip_address


@method_decorator(requires_csrf_token, name='dispatch')
class ContactMessageFormView(FormView):
    template_name = 'contact_us/message_form.html'
    model = ContactMessage
    form_class = ContactMessageForm
    success_url = reverse_lazy('contact')

    def get_context_data(self, **kwargs):
        context = super(ContactMessageFormView, self).get_context_data(**kwargs)
        context.update(PAGE_CONTEXT)
        return context

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.save()
        messages.success(self.request,
                         "Thank you for contacting us, we will review your message and respond to your email "
                         "address, {}, if needed!".format(form.data.get('email')))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self):
        return {'ip_address': get_ip_address(self.request)}
