from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from education_content.forms import ChapterForm
from education_content.models import Chapter


class ChapterCreateView(LoginRequiredMixin, CreateView):
    model = Chapter
    form_class = ChapterForm
    success_url = reverse_lazy('education_content:list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ChapterUpdateView(LoginRequiredMixin, UpdateView):
    model = Chapter
    form_class = ChapterForm

    def get_success_url(self):
        return reverse('education_content:view', args=[self.kwargs.get('pk')])


class ChapterListView(LoginRequiredMixin, ListView):
    model = Chapter

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            # Make Q-objects for filtering
            published_condition = Q(is_published=True)
            owner_condition = Q(owner=self.request.user)
            # Combine them
            final_condition = published_condition | owner_condition
            # Filtering queryset
            queryset = queryset.filter(final_condition)
        return queryset


class ChapterDetailView(LoginRequiredMixin, DetailView):
    model = Chapter

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1  # Increment the views count when viewing a Chapter
        self.object.save()
        return self.object


class ChapterDeleteView(LoginRequiredMixin, DeleteView):
    model = Chapter
    success_url = reverse_lazy('education_content:list')  # Redirect to the list of Chapters after deleting a Chapter
