from django.contrib import admin

from unique_content.models import FigureFromP3din, FigureThinSection, Mineral, Label, Figure360View


@admin.register(FigureFromP3din)
class FigureFromP3dinAdmin(admin.ModelAdmin):
    # Define how the FigureFromP3din model is displayed in the Django admin panel.

    list_filter = ('title',)


@admin.register(FigureThinSection)
class FigureThinSectionAdmin(admin.ModelAdmin):
    # Define how the FigureThinSection model is displayed in the Django admin panel.
    list_filter = ('title',)


@admin.register(Mineral)
class MineralAdmin(admin.ModelAdmin):
    # Define how the Mineral model is displayed in the Django admin panel.
    list_filter = ('name_eng',)


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    # Define how the Label model is displayed in the Django admin panel.
    list_filter = ('figure_thin_section',)


@admin.register(Figure360View)
class Figure360ViewAdmin(admin.ModelAdmin):
    # Define how the Figure360View model is displayed in the Django admin panel.

    list_filter = ('title',)
