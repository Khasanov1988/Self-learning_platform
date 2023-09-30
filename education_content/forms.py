from django import forms

from education_content.models import Chapter
from users.forms import StyleFormMixin


class ChapterForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ('title', 'description', 'preview',)
