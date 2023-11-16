from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from unique_content.models import FigureThinSection


class FigureThinSectionDetailView(LoginRequiredMixin, DetailView):
    model = FigureThinSection