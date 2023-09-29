from django.urls import path

from education_content.apps import EducationContentConfig
from education_content.views import ChapterCreateView, ChapterListView, ChapterDetailView, ChapterUpdateView, \
    ChapterDeleteView

app_name = EducationContentConfig.name

urlpatterns = [
    # URL pattern for creating a new post
    path('create/', ChapterCreateView.as_view(), name='create'),

    # URL pattern for listing posts with a 60-second cache timeout
    path('', ChapterListView.as_view(), name='list'),

    # URL pattern for viewing a single post
    path('view/<int:pk>/', ChapterDetailView.as_view(), name='view'),

    # URL pattern for editing an existing post
    path('edit/<int:pk>/', ChapterUpdateView.as_view(), name='edit'),

    # URL pattern for deleting an existing post
    path('delete/<int:pk>/', ChapterDeleteView.as_view(), name='delete'),
]
