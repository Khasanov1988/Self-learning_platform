from django import forms
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from education_content.models import Chapter, Material, MaterialPhotos
from users.forms import StyleFormMixin


class ChapterForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ('title', 'description', 'preview',)


class MaterialForm(StyleFormMixin, forms.ModelForm):
    text = SummernoteTextField()
    class Meta:
        model = Material
        fields = ('topic', 'description', 'text', 'preview', 'chapter',)
        widgets = {
            'text': SummernoteInplaceWidget(),
        }


class MaterialUpdateForm(StyleFormMixin, forms.ModelForm):
    text = SummernoteTextField()
    class Meta:
        model = Material
        fields = ('topic', 'description', 'text', 'preview',)
        widgets = {
            'text': SummernoteInplaceWidget(),
        }


class MaterialForChapterForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Material
        fields = ('topic', 'description', 'text', 'preview',)


class MaterialPhotosForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MaterialPhotos
        fields = ('signature', 'figure', 'material',)
