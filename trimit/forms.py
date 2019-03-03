from django import forms
from django.contrib.auth.models import User
from trimit.models import UserProfile


# class loginForm(forms.ModelForm):



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


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({'id': 'profile-picture-field'})
