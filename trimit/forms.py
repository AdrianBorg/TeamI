from django import forms
from django.contrib.auth.models import User
from trimit.models import UserProfile, Page
from django_countries.widgets import CountrySelectWidget


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id': 'username-field'})
        self.fields['email'].widget.attrs.update({'id': 'email-field',
                                                  'placeholder': 'user@trimit.com'},)
        self.fields['email'].required = True
        self.fields['password'].widget.attrs.update({'id': 'password-field'})


class HairdresserPageForm(forms.ModelForm):
    opening_times = forms.CharField(
        max_length=300,
        widget=forms.Textarea,
    )

    class Meta:
        model = Page
        fields = ('name', 'flat_number', 'street_address', 'city', 'postcode', 'country', 'opening_times',
                  'contact_number', 'profile_picture', 'webpage', 'instagram',)
        widgets = {'country': CountrySelectWidget(
            layout='<div class="country-widget">{widget}<img class="country-select-flag" id="{flag_id}" style="margin: 6px 0 0 4px" src="{country.flag}"></div>'
        )}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Display name'
        self.fields['name'].widget.attrs.update({'id': 'name-field'})
        self.fields['flat_number'].widget.attrs.update({'id': 'flat_number-field'})
        self.fields['street_address'].widget.attrs.update({'id': 'street_address-field'})
        self.fields['city'].widget.attrs.update({'id': 'city-field'})
        self.fields['postcode'].widget.attrs.update({'id': 'postcode-field'})
        self.fields['country'].widget.attrs.update({'id': 'country-field'})
        self.fields['opening_times'].widget.attrs.update({'id': 'opening_times-field'})
        self.fields['contact_number'].widget.attrs.update({'id': 'contact_number-field'})
        self.fields['webpage'].widget.attrs.update({'id': 'webpage-field'})
        self.fields['instagram'].widget.attrs.update({'id': 'instagram-field'})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({'id': 'profile-picture-field'})

