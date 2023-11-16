from django.db import models
from django.utils import timezone

from config import settings


class FigureFromP3din(models.Model):
    """
    3d figures from p3d.in class
    """
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.CharField(max_length=500, verbose_name='Description')
    preview = models.ImageField(null=True, blank=True, verbose_name='Preview')
    link = models.CharField(max_length=300, verbose_name='Link to p3d.in')
    made_date = models.DateTimeField(default=timezone.now, verbose_name='Creation time')
    last_update = models.DateTimeField(default=timezone.now, verbose_name='Last update time')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Owner')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = '3D figure'
        verbose_name_plural = '3D figures'


class FigureThinSection(models.Model):
    """
    Figure for thin sections
    """
    title = models.CharField(max_length=100, verbose_name='Rock title')
    description = models.CharField(max_length=500, verbose_name='Description')
    preview = models.ImageField(null=True, blank=True, verbose_name='Preview')
    file_ppl = models.FileField(null=True, blank=True, default=None, verbose_name='File PPL')
    file_cpl = models.FileField(null=True, blank=True, default=None, verbose_name='File CPL')
    made_date = models.DateTimeField(default=timezone.now, verbose_name='Creation time')
    last_update = models.DateTimeField(default=timezone.now, verbose_name='Last update time')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Owner')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Thin Section'
        verbose_name_plural = 'Thin Sections'
