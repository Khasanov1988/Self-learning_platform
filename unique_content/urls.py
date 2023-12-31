from django.urls import path
from unique_content.apps import UniqueContentConfig
from unique_content.views import FigureThinSectionDetailView, FigureFromP3dinDetailView, FigureThinSectionListView, \
    FigureFromP3dinListView

app_name = UniqueContentConfig.name

urlpatterns = [
    # URL pattern for viewing a single thin_section
    path('virtual_microscope/<int:pk>/', FigureThinSectionDetailView.as_view(), name='thin_section_view'),
    path('3d_model/<int:pk>/', FigureFromP3dinDetailView.as_view(), name='model_3d_view'),
    path('virtual_microscope_list/', FigureThinSectionListView.as_view(), name='thin_section_list'),
    path('3d_model_list/', FigureFromP3dinListView.as_view(), name='model_3d_list'),
]
