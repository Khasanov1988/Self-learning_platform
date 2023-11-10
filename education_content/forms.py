import requests
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
            'text': SummernoteWidget(),
        }


class MaterialUpdateForm(StyleFormMixin, forms.ModelForm):
    text = SummernoteTextField()

    class Meta:
        model = Material
        fields = ('topic', 'description', 'text', 'preview',)
        widgets = {
            'text': SummernoteWidget(),
        }


class MaterialForChapterForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Material
        fields = ('topic', 'description', 'text', 'preview',)


class MaterialPhotosForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MaterialPhotos
        fields = ('signature', 'figure', 'figure_3d', 'material',)

    def clean(self):
        cleaned_data = super().clean()
        figure_3d = cleaned_data.get('figure_3d')
        figure = cleaned_data.get('figure')
        # Checking for completion of at least one field
        if figure_3d or figure:
            # Checking the correctness of the link to the p3d.in service
            if figure_3d:
                response = requests.get(figure_3d)
                status_code = response.status_code
                if not (figure_3d[0:15] == 'https://p3d.in/' and status_code == 200):
                    self.add_error('figure_3d', 'Invalid p3d.in link')
                cleaned_data['figure_3d'] = f'{figure_3d[0:15]}e/{figure_3d[15:]}+spin'
        else:
            self.add_error('figure', 'Should be at least one field not empty')

        return cleaned_data
