from django import forms
from trimit.models import EUser, UserProfile


class EUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = EUser
        fields = ('username', 'email', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id': 'username-field'})
        self.fields['email'].widget.attrs.update({'id': 'email-field',
                                                  'placeholder': 'user@trimit.com'},)
        self.fields['password'].widget.attrs.update({'id': 'password-field'})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({'id': 'profile-picture-field'})
