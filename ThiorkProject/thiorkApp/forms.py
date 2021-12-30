from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, DateTimeField
from location_field.models.plain import PlainLocationField

from .models import Servitium, Vectis, Eventum
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


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class EventumForm(ModelForm, forms.Form):
    location = PlainLocationField(based_fields=['city'])
    date = DateTimeField(widget=DateTimeInput)

    class Meta:
        model = Eventum
        fields = ['title', 'description', 'max_number_of_attendees', 'city', 'date', 'location', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].label = "Enter a location for this eventum"
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Save'))
