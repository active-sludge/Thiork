from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from location_field.models.plain import PlainLocationField

from .models import Servitium, Vectis
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column


class VectisForm(UserCreationForm):
    class Meta:
        model = Vectis
        fields = [
            'username',
            'email',
            'bio',
            'photo',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('sign_up', 'Sign Up'))


class ServitiumForm(ModelForm, forms.Form):
    location = PlainLocationField(based_fields=['city'])

    class Meta:
        model = Servitium
        fields = ['title', 'description', 'city', 'location', 'credit', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].label = "Enter a location for this servitium"
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Save'))
