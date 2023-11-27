from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django.forms import BooleanField

from users.models import User


class StyleFormMixin:
    """
    Add form-control to necessary forms
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserProfileForm(StyleFormMixin, UserChangeForm):
    password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        required=False,
    )
    password2 = forms.CharField(
        label="New password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        required=False,
    )

    class Meta:
        model = User
        fields = ('email', 'FIO', 'phone', 'comment', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        model = User

    def clean_username(self):
        return self.cleaned_data['username'].lower()
