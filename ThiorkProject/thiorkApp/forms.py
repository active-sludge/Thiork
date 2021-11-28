from django.forms import ModelForm
from .models import Servitium
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column


class ServitiumForm(ModelForm):
    class Meta:
        model = Servitium
        fields = ['title', 'description', 'location', 'credit', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Save'))
