from django import forms
from django.utils.translation import ugettext as _
from django.contrib import messages

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    bot_field = forms.CharField(required=False,
                                max_length=50,
                                label='Tag',
                                help_text=_('Please tag the comment appropriately.'),
                                widget=forms.HiddenInput())

    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'subject', 'message', 'ip_address')
        widgets = {
            'subject': forms.Select(attrs={'class': 'select-input-fill'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'label': 'Name',
                                           'placeholder': 'Jane Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'your@email.com'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': '2',
                                             'placeholder': 'What is on your mind?'}),
            'ip_address': forms.HiddenInput()
        }

    def clean_bot_field(self):
        value = self.cleaned_data["bot_field"]
        if value:
            raise forms.ValidationError(_("Do not enter anything into this field, unless you are a computer."),
                                        code='invalid')

        return value

    def clean(self):
        cleaned_data = super(ContactMessageForm, self).clean()
        ip_address = cleaned_data.get('ip_address')
        if not ip_address or not self.Meta.model.can_post(ip_address):
            raise forms.ValidationError(_('Cannot accept posts at this time.'), code='invalid')
        if self.Meta.model.is_duplicate(self.instance):
            raise forms.ValidationError(_('This appears to be a duplicate?'), code='invalid')

        return cleaned_data

    # def save(self, commit=True):
    #     if self.errors:
    #         raise ValueError(
    #             "The %s could not be %s because the data didn't validate." % (
    #                 self.instance._meta.object_name,
    #                 'created' if self.instance._state.adding else 'changed',
    #             )
    #         )
    #     if commit:
    #         self.instance.save()
    #         messages.success(request,
    #                          "Thank you for contacting us, we will review your message and respond to your email "
    #                          "address, {}, if needed!".format(self.instance.email))
    #     return self.instance
