from django.contrib import admin

from education_content.models import Chapter, Material, MaterialPhotos


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    # Define how the Chapter model is displayed in the Django admin panel.

    list_filter = ('title',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    # Define how the Chapter model is displayed in the Django admin panel.
    list_filter = ('topic',)


@admin.register(MaterialPhotos)
class MaterialPhotosAdmin(admin.ModelAdmin):
    # Define how the Chapter model is displayed in the Django admin panel.

    list_filter = ('signature',)
