from django.urls import path
from unique_content.apps import UniqueContentConfig
from unique_content.views import FigureThinSectionDetailView, FigureFromP3dinDetailView

app_name = UniqueContentConfig.name

urlpatterns = [
    # URL pattern for viewing a single thin_section
    path('thin_section_view/<int:pk>/', FigureThinSectionDetailView.as_view(), name='thin_section_view'),
    path('model_3d/<int:pk>/', FigureFromP3dinDetailView.as_view(), name='model_3d_view'),
]
