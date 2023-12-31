from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from unique_content.models import FigureThinSection, FigureFromP3din


class FigureThinSectionDetailView(LoginRequiredMixin, DetailView):
    model = FigureThinSection

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        labels_list = self.object.label_set.all().select_related('mineral')
        context_data['labels_list'] = labels_list
        return context_data


class FigureThinSectionListView(LoginRequiredMixin, ListView):
    model = FigureThinSection


class FigureFromP3dinDetailView(LoginRequiredMixin, DetailView):
    model = FigureFromP3din


class FigureFromP3dinListView(LoginRequiredMixin, ListView):
    model = FigureFromP3din
