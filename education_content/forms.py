from django import forms

from education_content.models import Chapter, Material
from users.forms import StyleFormMixin


class ChapterForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ('title', 'description', 'preview',)


class MaterialForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Material
        fields = ('topic', 'description', 'text', 'preview', 'chapter')


class MaterialForChapterForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Material
        fields = ('topic', 'description', 'text', 'preview',)
