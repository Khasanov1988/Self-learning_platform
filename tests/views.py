from django.apps import apps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView

from education_content.models import Material
from education_content.views import GetFinalConditionsMixin, GetLastUpdateMixin
from tests.forms import *
from tests.models import *


@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def change_published_status(request, model: str, pk: int):
    """
    Change publication or publication request status
    """
    got_model = apps.get_model('tests', model)
    try:
        got_object = got_model.objects.get(pk=pk)
    except got_model.DoesNotExist:
        raise Http404("Object not found")

    current_value = getattr(got_object, 'is_published')
    new_value = not current_value
    setattr(got_object, 'is_published', new_value)
    got_object.is_published_requested = False
    got_object.save()
    return redirect(reverse(f'tests:{model.lower()}_view', kwargs={'pk': pk}))


@login_required
def change_published_requested_status(request, model: str, pk: int):
    """
    Change publication request status
    """
    got_model = apps.get_model('tests', model)
    try:
        got_object = got_model.objects.get(pk=pk)
    except got_model.DoesNotExist:
        raise Http404("Object not found")

    if not (got_object.owner == request.user or request.user.is_staff):
        raise Http404("Access denied")

    current_value = getattr(got_object, 'is_published_requested')
    new_value = not current_value
    setattr(got_object, 'is_published_requested', new_value)
    got_object.save()
    return redirect(reverse(f'tests:{model.lower()}_view', kwargs={'pk': pk}))


class GetMaterialListMixin:
    """
    Include material list in context
    """

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        material_list = Material.objects.all()
        context_data['material_list'] = material_list
        return context_data


class TestCreateView(LoginRequiredMixin, GetMaterialListMixin, CreateView):
    model = Test
    form_class = TestForm
    success_url = reverse_lazy('tests:test_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class TestCreateMaterialView(LoginRequiredMixin, GetMaterialListMixin, CreateView):
    model = Test
    form_class = TestForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['material_pk'] = self.kwargs['material_pk']
        return context_data

    def get_success_url(self):
        # We dynamically construct the URL using reverse_lazy and the value of material_pk
        material_pk = self.kwargs['material_pk']
        return reverse_lazy('education_content:material_view', kwargs={'pk': material_pk})


class TestUpdateView(LoginRequiredMixin, GetLastUpdateMixin, UpdateView):
    model = Test
    form_class = TestUpdateForm

    def get_success_url(self):
        return reverse('tests:test_view', args=[self.kwargs.get('pk')])


class TestListView(LoginRequiredMixin, GetFinalConditionsMixin, ListView):
    model = Test

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            queryset = queryset.filter(self.get_final_conditions())
        return queryset


class TestDetailView(LoginRequiredMixin, GetFinalConditionsMixin, DetailView):
    model = Test

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1  # Increment the views count when viewing a Test
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        question_list = self.object.question_set.all()
        context_data['question_list'] = question_list
        return context_data


class TestDeleteView(LoginRequiredMixin, DeleteView):
    model = Test
    success_url = reverse_lazy(
        'tests:test_list')  # Redirect to the list of Chapters after deleting a Chapter
