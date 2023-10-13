from tests.apps import TestsConfig
from django.urls import path

from tests.views import *

app_name = TestsConfig.name

urlpatterns = [
    # View to change published status
    path('view/changepublishedstatus/<str:model>/<int:pk>/', change_published_status,
         name='change_published_status'),

    # View to change some status
    path('view/changepublishedrequestedstatus/<str:model>/<int:pk>/', change_published_requested_status,
         name='change_published_requested_status'),

    # URL pattern for creating a new tests
    path('test_create/', TestCreateView.as_view(), name='test_create'),

    # URL pattern for listing tests
    path('', TestListView.as_view(), name='test_list'),

    # URL pattern for viewing a single test
    path('test_view/<int:pk>/', TestDetailView.as_view(), name='test_view'),

    # URL pattern for editing an existing test
    path('test_edit/<int:pk>/', TestUpdateView.as_view(), name='test_edit'),

    # URL pattern for deleting an existing test
    path('test_delete/<int:pk>/', TestDeleteView.as_view(), name='test_delete'),

    # URL pattern for creating a new completed tests
    path('test_run/<int:test_pk>/', TestRunView.as_view(), name='test_run'),
]
