from django import forms

from tests.models import *
from users.forms import StyleFormMixin


class TestForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title', 'description', 'material', 'owner', 'is_published', 'is_published_requested',)


class TestUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title', 'description', 'owner', 'is_published', 'is_published_requested',)