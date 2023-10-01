from django.db import models
from django.utils import timezone

from config import settings


class Chapter(models.Model):
    """
    Chapter class
    """
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.CharField(max_length=500, verbose_name='Description')
    preview = models.ImageField(null=True, blank=True, verbose_name='Preview')
    made_date = models.DateField(default=timezone.now, verbose_name='Creation date')
    last_update = models.DateField(default=None, null=True, blank=True, verbose_name='Last update date')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Owner')
    is_published = models.BooleanField(default=False, verbose_name='Publication Status')
    is_published_requested = models.BooleanField(default=False, verbose_name='Publication request status')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Number of Views')

    def __str__(self):
        return f'Chapter - {self.title}'

    class Meta:
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'
        permissions = [
            (
                'set_published',
                'Can publish posts'
            )
        ]


class Material(models.Model):
    """
    Educational material class
    """
    topic = models.CharField(max_length=100, verbose_name='Title')
    description = models.CharField(max_length=300, null=True, blank=True, verbose_name='Description')
    text = models.TextField(verbose_name='Text')
    preview = models.ImageField(null=True, blank=True, verbose_name='Preview')
    made_date = models.DateField(default=timezone.now, verbose_name='Creation date')
    last_update = models.DateField(default=None, null=True, blank=True, verbose_name='Last update date')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Owner')
    chapter = models.ForeignKey('education_content.Chapter', on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False, verbose_name='Publication status')
    is_published_requested = models.BooleanField(default=False, verbose_name='Publication request status')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Number of views')

    def __str__(self):
        return f'Material - {self.topic}'

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'
        permissions = [
            (
                'set_published',
                'Can publish posts'
            )
        ]


class MaterialPhotos(models.Model):
    """
    Material figures
    """
    signature = models.CharField(max_length=100, default=None, null=True, blank=True, verbose_name='Signature')
    figure = models.ImageField(verbose_name='Figure')
    material = models.ForeignKey('education_content.Material', on_delete=models.CASCADE)

    def __str__(self):
        return f'Figure - {self.signature}'

    class Meta:
        verbose_name = 'Figure'
        verbose_name_plural = 'Figures'

