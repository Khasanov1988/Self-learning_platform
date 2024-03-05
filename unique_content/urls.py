from django.urls import path
from unique_content.apps import UniqueContentConfig
from unique_content.views import FigureThinSectionDetailView, FigureFromP3dinDetailView, FigureThinSectionListView, \
    FigureFromP3dinListView, Figure360ViewDetailView, Figure360ViewListView, FigureMapDetailView, FigureMapListView, \
    calculate_real_north, set_north_to_zero

app_name = UniqueContentConfig.name

urlpatterns = [
    # URL pattern for viewing a single thin_section
    path('virtual_microscope/<int:pk>/', FigureThinSectionDetailView.as_view(), name='thin_section_view'),
    path('3d_model/<int:pk>/', FigureFromP3dinDetailView.as_view(), name='model_3d_view'),
    path('virtual_microscope_list/', FigureThinSectionListView.as_view(), name='thin_section_list'),
    path('3d_model_list/', FigureFromP3dinListView.as_view(), name='model_3d_list'),
    path('360view/<int:pk>/', Figure360ViewDetailView.as_view(), name='360view_view'),
    path('360view_list/', Figure360ViewListView.as_view(), name='360view_list'),
    path('map/<int:pk>/', FigureMapDetailView.as_view(), name='map_view'),
    path('map_list/', FigureMapListView.as_view(), name='map_list'),
    path('360view/calculaterealnorth/<int:pk>/', calculate_real_north, name='calculate_real_north'),
    path('360view/setnorthtozero/<int:pk>/', set_north_to_zero, name='set_north_to_zero'),
]
