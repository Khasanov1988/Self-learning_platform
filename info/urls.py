from info.apps import InfoConfig
from django.urls import path

from info.views import PrivacyPolicy

app_name = InfoConfig.name

urlpatterns = [
    # URL pattern for creating a new tests
    path('privacy_policy/', PrivacyPolicy.as_view(), name='test_create'),
]
