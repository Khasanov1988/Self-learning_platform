from django.urls import path

from education_content.apps import EducationContentConfig
from education_content.views import *

app_name = EducationContentConfig.name

urlpatterns = [
    # URL pattern for creating a new chapter
    path('chapter_create/', ChapterCreateView.as_view(), name='chapter_create'),

    # URL pattern for listing chapter with a 60-second cache timeout
    path('', ChapterListView.as_view(), name='chapter_list'),

    # URL pattern for viewing a single chapter
    path('chapter_view/<int:pk>/', ChapterDetailView.as_view(), name='chapter_view'),

    # URL pattern for editing an existing chapter
    path('chapter_edit/<int:pk>/', ChapterUpdateView.as_view(), name='chapter_edit'),

    # URL pattern for deleting an existing chapter
    path('chapter_delete/<int:pk>/', ChapterDeleteView.as_view(), name='chapter_delete'),

    # View to change published status
    path('view/changepublishedstatus/<str:model>/<int:pk>/', change_published_status,
         name='change_published_status'),

    # View to change some status
    path('view/changepublishedrequestedstatus/<str:model>/<int:pk>/', change_published_requested_status,
         name='change_published_requested_status'),

    # URL pattern for listing material with a 60-second cache timeout
    # TODO: Исправить chapter на material
    path('', ChapterListView.as_view(), name='material_list'),

    # URL pattern for viewing a single material
    # TODO: Исправить chapter на material
    path('chapter_view/<int:pk>/', ChapterDetailView.as_view(), name='material_view'),

]
