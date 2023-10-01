from django.apps import apps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from education_content.forms import ChapterForm
from education_content.models import Chapter, Material


class GetFinalConditionsMixin:
    """
    Mixin adding method filtering formset based on publication and belonging to an authenticated user
    """

    def get_final_conditions(self):
        # Make Q-objects for filtering
        published_condition = Q(is_published=True)
        owner_condition = Q(owner=self.request.user)
        # Combine them
        return published_condition | owner_condition


class ChapterCreateView(LoginRequiredMixin, CreateView):
    model = Chapter
    form_class = ChapterForm
    success_url = reverse_lazy('education_content:chapter_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ChapterUpdateView(LoginRequiredMixin, UpdateView):
    model = Chapter
    form_class = ChapterForm

    def get_success_url(self):
        return reverse('education_content:chapter_view', args=[self.kwargs.get('pk')])


class ChapterListView(LoginRequiredMixin, GetFinalConditionsMixin, ListView):
    model = Chapter

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            queryset = queryset.filter(self.get_final_conditions())
        return queryset


class ChapterDetailView(LoginRequiredMixin, GetFinalConditionsMixin, DetailView):
    model = Chapter

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1  # Increment the views count when viewing a Chapter
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        material_list = self.object.material_set.all()
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            material_list = material_list.filter(self.get_final_conditions())
        context_data['material_list'] = material_list
        return context_data


class ChapterDeleteView(LoginRequiredMixin, DeleteView):
    model = Chapter
    success_url = reverse_lazy('education_content:chapter_list')  # Redirect to the list of Chapters after deleting a Chapter


@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def change_published_status(request, model: str, pk: int):
    """
    Change publication or publication request status
    """
    got_model = apps.get_model('education_content', model)
    try:
        got_object = got_model.objects.get(pk=pk)
    except got_model.DoesNotExist:
        raise Http404("Object not found")

    current_value = getattr(got_object, 'is_published')
    new_value = not current_value
    setattr(got_object, 'is_published', new_value)
    if not got_object.is_published:
        got_object.is_published_requested = False
    got_object.save()
    return redirect(reverse(f'education_content:{model.lower()}_view', kwargs={'pk': pk}))


@login_required
def change_published_requested_status(request, model: str, pk: int):
    """
    Change publication request status
    """
    got_model = apps.get_model('education_content', model)
    try:
        got_object = got_model.objects.get(pk=pk)
    except got_model.DoesNotExist:
        raise Http404("Object not found")

    if got_object.owner != request.user:
        raise Http404("Access denied")

    current_value = getattr(got_object, 'is_published_requested')
    new_value = not current_value
    setattr(got_object, 'is_published_requested', new_value)
    got_object.save()
    return redirect(reverse(f'education_content:{model.lower()}_view', kwargs={'pk': pk}))
