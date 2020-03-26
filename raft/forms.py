from django.forms import ModelForm
from django.forms import ModelMultipleChoiceField
from django.conf import settings
from .models import Contact
from services.models import Service
from .tasks import send_email_async


class ContactForm(ModelForm):
    services = ModelMultipleChoiceField(
        queryset=Service.objects,
        required=False
    )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message', 'services']

    def send_email(self):
        name = self.cleaned_data['name']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        send_email_async.delay(
            subject=f'New message from {name}: {subject}',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.DEFAULT_TO_EMAIL
        )
