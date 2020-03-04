from django.forms import ModelForm
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['interests', 'photo']
