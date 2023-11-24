from django import forms
from django.core.exceptions import ValidationError
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from education_content.models import Chapter, Material, MaterialPhotos
from users.forms import StyleFormMixin


class ChapterForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ('title', 'description', 'preview',)

    def clean_preview(self):
        preview = self.cleaned_data.get('preview')

        if preview:
            # Ограничение размера изображения до 2 МБ
            max_size = 5 * 1024 * 1024  # 2 МБ в байтах

            if preview.size > max_size:
                self.add_error('preview', 'The image size should be no more than 5 MB')
                raise forms.ValidationError('The image size should be no more than 5 MB')

            # Опционально, вы также можете проверить тип файла (изображение)
            content_type = preview.content_type.split('/')[0]
            if content_type not in ['image']:
                self.add_error('preview', 'File type is not supported. Please upload an image')
                raise forms.ValidationError('File type is not supported. Please upload an image')

            # Опционально, вы также можете проверить размеры изображения, например, ширина и высота
            # image = Image.open(preview)
            # if image.width > some_width or image.height > some_height:
            #     raise forms.ValidationError('The image dimensions should be within certain limits.')

        return preview


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
        fields = ('signature', 'material', 'thin_section', 'p3din_model',)

    def clean(self):
        cleaned_data = super().clean()
        field1 = cleaned_data.get('thin_section')
        field2 = cleaned_data.get('p3din_model')

        # Checking if only one of the fields is filled in
        if field1 and field2:
            self.add_error('p3din_model', 'Only one of thin_section and p3din_model can be filled at a time')
            raise ValidationError("Only one of thin_section and p3din_model can be filled at a time")


        return cleaned_data
