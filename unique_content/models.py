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
    link = models.URLField(max_length=300, verbose_name='Link to p3d.in')
    link_for_iframe = models.URLField(max_length=302, null=True, blank=True, verbose_name='Link to p3d.in iframe')
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
    preview_ppl = models.ImageField(null=True, blank=True, verbose_name='Preview PPL')
    preview_cpl = models.ImageField(null=True, blank=True, verbose_name='Preview CPL')
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


class Mineral(models.Model):
    """
    Mineral
    """
    name_eng = models.CharField(max_length=100, verbose_name='Mineral name(Eng)')
    name_rus = models.CharField(max_length=100, verbose_name='Mineral name(Rus)')
    abbreviation = models.CharField(max_length=7, verbose_name='Mineral abbreviation')

    def __str__(self):
        return f'{self.abbreviation}'

    class Meta:
        verbose_name = 'Mineral'
        verbose_name_plural = 'Minerals'


class Label(models.Model):
    """
    Signature label
    """
    mineral = models.ForeignKey('unique_content.Mineral', on_delete=models.CASCADE)
    figure_thin_section = models.ForeignKey('unique_content.FigureThinSection', on_delete=models.CASCADE)
    coord_X = models.DecimalField(decimal_places=1, max_digits=3, default=0.00, verbose_name='Label X coordinate on the video')
    coord_Y = models.DecimalField(decimal_places=1, max_digits=3, default=0.00, verbose_name='Label Y coordinate on the video')

    def __str__(self):
        return f'Label id: {self.pk}'

    class Meta:
        verbose_name = 'Mineral signature label'
        verbose_name_plural = 'Mineral signature labels'
