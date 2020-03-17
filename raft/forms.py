from django.forms import forms
from django.forms import ChoiceField
from django.forms.widgets import RadioSelect
from .models import Category


class EstimateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        model_id = kwargs.pop('initial')['model_id']
        self.model = Category.objects.filter(id=model_id).first()
        super().__init__(*args, **kwargs)
        choices = tuple(
            (service.id, service.name)
            for service in self.model.service_set.all()
        )
        self.fields['services'] = ChoiceField(
            choices=choices,
            widget=RadioSelect(attrs={'class': 'radio'})
        )
