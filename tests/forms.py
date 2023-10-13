from django import forms

from tests.models import *
from users.forms import StyleFormMixin


class TestForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title', 'description', 'material', 'preview', 'owner', 'is_published', 'is_published_requested',)


class TestUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title', 'description', 'preview', 'owner', 'is_published', 'is_published_requested',)


class CompletedTestForm(forms.ModelForm):
    class Meta:
        model = CompletedTest
        fields = ('test', 'user', 'passed_time',)
