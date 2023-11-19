from django.contrib import admin

from unique_content.models import FigureFromP3din, FigureThinSection, Mineral


@admin.register(FigureFromP3din)
class FigureFromP3dinAdmin(admin.ModelAdmin):
    # Define how the Chapter model is displayed in the Django admin panel.

    list_filter = ('title',)


@admin.register(FigureThinSection)
class FigureThinSectionAdmin(admin.ModelAdmin):
    # Define how the Material model is displayed in the Django admin panel.
    list_filter = ('title',)

@admin.register(Mineral)
class MineralAdmin(admin.ModelAdmin):
    # Define how the Material model is displayed in the Django admin panel.
    list_filter = ('title',)

@admin.register(Label)
class MineralAdmin(admin.ModelAdmin):
    # Define how the Material model is displayed in the Django admin panel.
    list_filter = ('title',)
