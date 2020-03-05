from django.forms import ModelForm
from .models import Profile
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('interests', 'photo')
        template_name = "settings.html"


class ProfileDeleteForm(ModelForm):
    class Meta:
        model = User
        fields = []
