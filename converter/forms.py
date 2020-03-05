from django.forms import ModelForm
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('interests', 'photo')
        template_name = "settings.html"

    # def __init__(self, *args, **kwargs):
    #     super(ProfileForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Fieldset(
    #             'first arg is the legend of the fieldset',
    #             'like_website',
    #             'favorite_number',
    #             'favorite_color',
    #             'favorite_food',
    #             'notes'
    #         ),
    #         ButtonHolder(
    #             Submit('submit', 'Submit', css_class='button white')
    #         )
    #     )
