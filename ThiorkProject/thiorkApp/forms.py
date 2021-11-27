from django.forms import ModelForm
from .models import Servitium


class ServitiumForm(ModelForm):
    class Meta:
        model = Servitium
        fields = ['title', 'description', 'location', 'credit', 'image']
