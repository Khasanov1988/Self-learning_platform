from PIL import Image
from django.db import models
from django.http import Http404
from django.utils import timezone
from config import settings

from unique_content.services import get_metadata_from_img, get_youtube_for_iframe_from_youtube, image_compression, \
    clean_old_data_for_view_field, haversine


class FigureFromP3din(models.Model):
    """
    3d figures from p3d.in class
    """
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.CharField(null=True, blank=True, max_length=2000, verbose_name='Description')
    autor = models.CharField(max_length=100, null=True, blank=True, verbose_name='Autor')
    preview = models.ImageField(null=True, blank=True, verbose_name='Preview')
    link = models.URLField(max_length=300, verbose_name='Link to p3d.in')
    link_for_iframe = models.URLField(max_length=302, null=True, blank=True, verbose_name='Link to p3d.in iframe')
    made_date = models.DateTimeField(default=timezone.now, verbose_name='Creation time')
    last_update = models.DateTimeField(default=timezone.now, verbose_name='Last update time')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Owner')
    is_login_required = models.BooleanField(default=True, verbose_name='Login required status')

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
    description = models.CharField(null=True, blank=True, max_length=2000, verbose_name='Description')
    view = models.ImageField(null=True, blank=True, verbose_name='View')
    autor = models.CharField(max_length=100, null=True, blank=True, verbose_name='Autor')
    preview = models.ImageField(null=True, blank=True, verbose_name='Preview')
    preview_ppl = models.ImageField(null=True, blank=True, verbose_name='Preview PPL')
    preview_cpl = models.ImageField(null=True, blank=True, verbose_name='Preview CPL')
    file_ppl = models.FileField(null=True, blank=True, default=None, verbose_name='File PPL')
    file_cpl = models.FileField(null=True, blank=True, default=None, verbose_name='File CPL')
    made_date = models.DateTimeField(default=timezone.now, verbose_name='Creation time')
    last_update = models.DateTimeField(default=timezone.now, verbose_name='Last update time')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Owner')
    is_login_required = models.BooleanField(default=True, verbose_name='Login required status')

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if self.view:
            clean_old_data_for_view_field(self, FigureThinSection)  # Call the function to clean old data
            compression_quality = 50
            new_size = {'width': 800, 'height': 400}
            compressed_image = image_compression(self.view, compression_quality, new_size)
            self.preview.save(f'{self.view.name[:-4]}_compressed{self.view.name[-4:]}', content=compressed_image,
                              save=False)
        super().save(*args, **kwargs)

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
    coord_X = models.DecimalField(decimal_places=1, max_digits=3, default=0.00,
                                  verbose_name='Label X coordinate on the video')
    coord_Y = models.DecimalField(decimal_places=1, max_digits=3, default=0.00,
                                  verbose_name='Label Y coordinate on the video')

    def __str__(self):
        return f'Label id: {self.pk}'

    class Meta:
        verbose_name = 'Mineral signature label'
        verbose_name_plural = 'Mineral signature labels'


class Figure360View(models.Model):
    """
    Figure for 360 view
    """
    TYPES = [
        ('air', 'Aerial panorama'),
        ('ground', 'Ground panorama'),
        ('other', 'Other type')
    ]

    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.CharField(null=True, blank=True, max_length=2000, verbose_name='Description')
    autor = models.CharField(max_length=100, null=True, blank=True, verbose_name='Autor')
    view = models.ImageField(verbose_name='View')
    preview = models.ImageField(null=True, blank=True, verbose_name='Preview')
    made_date = models.DateTimeField(default=timezone.now, verbose_name='Creation time')
    last_update = models.DateTimeField(default=timezone.now, verbose_name='Last update time')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Owner')
    is_login_required = models.BooleanField(default=True, verbose_name='Login required status')
    latitude = models.FloatField(null=True, blank=True, verbose_name='Latitude')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Longitude')
    height = models.FloatField(null=True, blank=True, verbose_name='Height')
    image_creation_date = models.DateTimeField(null=True, blank=True, verbose_name='Image Creation Date')
    pano_type = models.CharField(max_length=6, default='air', choices=TYPES, verbose_name='Panorama type')
    north_correction_angle = models.FloatField(default=0, verbose_name='North correction')

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        clean_old_data_for_view_field(self, Figure360View)  # Call the function to clean old data
        if self.view:
            image_creation_date_from_file, latitude_from_file, longitude_from_file, height_from_file = get_metadata_from_img(
                self.view)
            if not self.image_creation_date:
                self.image_creation_date = image_creation_date_from_file
            if not self.latitude:
                self.latitude = latitude_from_file
            if not self.longitude:
                self.longitude = longitude_from_file
            if not self.height:
                self.height = height_from_file

            compression_quality = 50
            new_size = {'width': 400, 'height': 200}
            compressed_image = image_compression(self.view, compression_quality, new_size)
            self.preview.save(f'{self.view.name[:-4]}_compressed{self.view.name[-4:]}', content=compressed_image,
                              save=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '360 view'
        verbose_name_plural = '360 views'


class Figure360ViewInterpretation(models.Model):
    """
    360 view interpretated view
    """

    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.CharField(null=True, blank=True, max_length=2000, verbose_name='Description')
    autor = models.CharField(max_length=100, null=True, blank=True, verbose_name='Autor')
    panorama = models.ForeignKey('unique_content.Figure360View', null=True, blank=True, on_delete=models.SET_NULL)
    view = models.ImageField(verbose_name='View')
    preview = models.ImageField(null=True, blank=True, verbose_name='Preview')
    made_date = models.DateTimeField(default=timezone.now, verbose_name='Creation time')
    last_update = models.DateTimeField(default=timezone.now, verbose_name='Last update time')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Owner')
    is_login_required = models.BooleanField(default=True, verbose_name='Login required status')

    def __str__(self):
        return f'{self.title} for {self.panorama}'

    def save(self, *args, **kwargs):
        clean_old_data_for_view_field(self, Figure360ViewInterpretation)  # Call the function to clean old data
        if self.view:
            compression_quality = 50
            new_size = {'width': 400, 'height': 200}
            compressed_image = image_compression(self.view, compression_quality, new_size)
            self.preview.save(f'{self.view.name[:-4]}_compressed{self.view.name[-4:]}', content=compressed_image,
                              save=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '360 view interpretation'
        verbose_name_plural = '360 view interpretations'


class InfoSpotForPanorama(models.Model):
    """
    Info spots for Panorama
    """
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.CharField(max_length=2000, null=True, blank=True, verbose_name='Description')
    link = models.URLField(null=True, blank=True, verbose_name='link')
    figure_3d = models.ForeignKey('unique_content.FigureFromP3din', null=True, blank=True, on_delete=models.SET_NULL)
    figure_thin_section = models.ForeignKey('unique_content.FigureThinSection', null=True, blank=True,
                                            on_delete=models.SET_NULL)
    preview = models.ImageField(null=True, blank=True, verbose_name='Preview')
    youtube = models.URLField(null=True, blank=True, verbose_name='Video link')
    youtube_for_iframe = models.URLField(null=True, blank=True, verbose_name='Iframe video link')
    latitude = models.FloatField(null=True, blank=True, verbose_name='Latitude')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Longitude')
    height = models.FloatField(null=True, blank=True, verbose_name='Height')

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if self.youtube:
            self.youtube_for_iframe = get_youtube_for_iframe_from_youtube(self.youtube)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Info spot'
        verbose_name_plural = 'Info spots'


class InfoSpotCoordinates(models.Model):
    """
    Info spots Coordinates
    """
    panorama = models.ForeignKey('unique_content.Figure360View', on_delete=models.CASCADE)
    info_spot = models.ForeignKey('unique_content.InfoSpotForPanorama', on_delete=models.CASCADE)
    is_reference = models.BooleanField(default=True, verbose_name='Is using as reference')
    distance = models.FloatField(null=True, blank=True, verbose_name='Distance between Panorama and InfoSpot')
    coord_X = models.FloatField(verbose_name='X coord')
    coord_Y = models.FloatField(verbose_name='Y coord')
    coord_Z = models.FloatField(verbose_name='Z coord')
    correction_angle = models.FloatField(null=True, blank=True, verbose_name='North correction angle')

    def __str__(self):
        return f'{self.panorama} --> {self.info_spot}'

    def save(self, *args, **kwargs):
        if not self.distance:
            if self.panorama.latitude and self.panorama.longitude and self.info_spot.latitude and self.info_spot.longitude:
                pano = self.panorama
                info_sp = self.info_spot
                self.distance = haversine(pano.latitude, pano.longitude, info_sp.latitude, info_sp.longitude,
                                          pano.height, info_sp.height)
            else:
                raise Http404(
                    'Impossible to canculate distance. One of your points has no coordinates. '
                    'You can set distance manually or include coordinates to both points')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Info spot coordinates'
        verbose_name_plural = 'Info spot coordinates'


class LinkSpotCoordinates(models.Model):
    """
    Link spots Coordinates
    """
    panorama_from = models.ForeignKey('unique_content.Figure360View', on_delete=models.CASCADE,
                                      related_name='panorama_from_coordinates')
    panorama_to = models.ForeignKey('unique_content.Figure360View', on_delete=models.CASCADE,
                                    related_name='panorama_to_coordinates')
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name='Title')
    distance = models.FloatField(null=True, blank=True, verbose_name='Distance between Panorama_From and Panorama_To')
    coord_X = models.FloatField(verbose_name='X coord')
    coord_Y = models.FloatField(verbose_name='Y coord')
    coord_Z = models.FloatField(verbose_name='Z coord')

    def __str__(self):
        return f'{self.panorama_from} --> {self.panorama_to}'

    def save(self, *args, **kwargs):
        if not self.distance:
            if self.panorama_from.latitude and self.panorama_from.longitude and self.panorama_to.latitude and self.panorama_to.longitude:
                pano_from = self.panorama_from
                pano_to = self.panorama_to
                self.distance = haversine(pano_from.latitude, pano_from.longitude, pano_to.latitude, pano_to.longitude,
                                          pano_from.height, pano_to.height)
            else:
                raise Http404(
                    'Impossible to canculate distance. One of your panoramas has no coordinates. '
                    'You can set distance manually or include coordinates to both panoramas')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Link spot coordinates'
        verbose_name_plural = 'Link spot coordinates'


class FigureMap(models.Model):
    """
    Figure for Map
    """

    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.CharField(null=True, blank=True, max_length=2000, verbose_name='Description')
    autor = models.CharField(max_length=100, null=True, blank=True, verbose_name='Autor')
    view = models.ImageField(null=True, blank=True, verbose_name='View')
    preview = models.ImageField(null=True, blank=True, verbose_name='Preview')
    map_file = models.FileField(null=True, blank=True, verbose_name='Map file')
    made_date = models.DateTimeField(default=timezone.now, verbose_name='Creation time')
    last_update = models.DateTimeField(default=timezone.now, verbose_name='Last update time')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Owner')
    is_login_required = models.BooleanField(default=True, verbose_name='Login required status')

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if self.view:
            clean_old_data_for_view_field(self, FigureMap)  # Call the function to clean old data
            compression_quality = 50
            new_height = 400  # explicitly set only the height
            try:
                # Open the image using PIL
                with Image.open(self.view) as img:
                    # Get the original width and height
                    original_width, original_height = img.size
                    if original_width and original_height:
                        aspect_ratio = original_width / original_height
                        new_width = int(new_height * aspect_ratio)
                        new_size = {'width': new_width, 'height': new_height}
                        compressed_image = image_compression(self.view, compression_quality, new_size)
                        self.preview.save(f'{self.view.name[:-4]}_compressed{self.view.name[-4:]}',
                                          content=compressed_image,
                                          save=False)
            except Exception as e:
                print(f"Error: {e}")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Map'
        verbose_name_plural = 'Maps'
