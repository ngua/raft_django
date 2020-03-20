from django.forms import forms, ModelForm
from django.forms import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from django.forms import ModelMultipleChoiceField
from .models import Category, Contact, Service


class EstimateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        model_id = kwargs.pop('initial')['model_id']
        self.model = Category.objects.filter(id=model_id).first()
        super().__init__(*args, **kwargs)
        choices = tuple(
            (service.id, service.name)
            for service in self.model.service_set.all()
        )
        self.fields['services'] = MultipleChoiceField(
            choices=choices,
            widget=CheckboxSelectMultiple(attrs={'class': 'checkbox'})
        )
        self.fields['services'].required = self.model.form_required
        self.legend = self.model.name

    @staticmethod
    def sum_price(*args):
        return sum(arg.price for arg in args)


class ContactForm(ModelForm):
    services = ModelMultipleChoiceField(
        queryset=Service.objects,
        required=False
    )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message', 'services']
