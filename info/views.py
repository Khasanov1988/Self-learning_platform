from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class PrivacyPolicy(TemplateView):
    template_name = 'info/privacy_policy.html'
