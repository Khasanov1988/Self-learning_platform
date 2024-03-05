import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView

from config.settings import GOOGLE_MAPS_KEY
from education_content.templatetags.my_tags import mediapath_filter
from education_content.views import LoginRequiredWithChoiceMixin
from unique_content.models import FigureThinSection, FigureFromP3din, Figure360View, InfoSpotForPanorama, \
    InfoSpotCoordinates, LinkSpotCoordinates, FigureMap
from unique_content.services import north_correction
from users.services import update_last_activity


@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def calculate_real_north(request, pk: int):
    """
    Calculating the true north of a panorama based on its coordinates and the coordinates of the InfoPoints it refers to
    """
    panorama = Figure360View.objects.get(pk=pk)
    info_spot_coords = (((InfoSpotCoordinates.objects.all().filter(panorama=pk, is_reference=True).exclude(
        coord_X=None)).exclude(coord_Y=None)).exclude(coord_Z=None))

    if len(info_spot_coords) > 0:
        info_spots = InfoSpotForPanorama.objects.all()
        north_correction(panorama, info_spot_coords, info_spots)
    else:
        raise Http404("Not enough links to InfoPoints")

    return redirect(reverse(f'unique_content:360view_view', kwargs={'pk': pk}))


@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def set_north_to_zero(request, pk: int):
    """
    Set North correction on current panorama to zero
    """
    panorama = Figure360View.objects.get(pk=pk)
    panorama.north_correction_angle = 0
    panorama.save()

    return redirect(reverse(f'unique_content:360view_view', kwargs={'pk': pk}))


class FigureThinSectionDetailView(LoginRequiredWithChoiceMixin, DetailView):
    model = FigureThinSection

    def get_context_data(self, **kwargs):
        update_last_activity(self.request.user)
        context_data = super().get_context_data()
        labels_list = self.object.label_set.all().select_related('mineral')
        context_data['labels_list'] = labels_list
        return context_data


class FigureThinSectionListView(LoginRequiredMixin, ListView):
    model = FigureThinSection
    ordering = ['-pk']


class FigureFromP3dinDetailView(LoginRequiredWithChoiceMixin, DetailView):
    model = FigureFromP3din

    def get_context_data(self, **kwargs):
        update_last_activity(self.request.user)
        context_data = super().get_context_data()
        return context_data


class FigureFromP3dinListView(LoginRequiredMixin, ListView):
    model = FigureFromP3din
    ordering = ['-pk']


class Figure360ViewDetailView(LoginRequiredWithChoiceMixin, DetailView):
    model = Figure360View

    def get_context_data(self, **kwargs):
        update_last_activity(self.request.user)
        context_data = super().get_context_data()
        pano_view_ids = [context_data['object'].pk]
        info_spot_queryset = InfoSpotForPanorama.objects.all().annotate(
            figure_thin_section_preview=F('figure_thin_section__preview'),
            figure_3d_link_for_iframe=F('figure_3d__link_for_iframe'))
        info_spot_queryset_filtered = (info_spot_queryset.filter(
            Q(infospotcoordinates__panorama_id__in=pano_view_ids)))
        info_spot_list = list(info_spot_queryset_filtered.values())
        info_spot_dict = {view['id']: view for view in info_spot_list}
        info_spot_coordinates_list = list(
            InfoSpotCoordinates.objects.filter(info_spot__in=info_spot_queryset_filtered).values())
        context_data['info_spot_dict'] = json.dumps(info_spot_dict)
        context_data['info_spot_coordinates_list'] = json.dumps(info_spot_coordinates_list)
        context_data['GOOGLE_MAPS_KEY'] = GOOGLE_MAPS_KEY

        figure_360_view_interpretation_list = self.object.figure360viewinterpretation_set.all().values('title', 'autor',
                                                                                                       'panorama',
                                                                                                       'view', )
        figure_360_view_interpretation_dict = {self.object.pk: list(figure_360_view_interpretation_list)}
        context_data['figure_360_view_interpretation_dict'] = json.dumps(figure_360_view_interpretation_dict)
        return context_data


class Figure360ViewListView(LoginRequiredMixin, ListView):
    model = Figure360View
    ordering = ['-pk']

    def get_context_data(self, **kwargs):
        update_last_activity(self.request.user)
        context_data = super().get_context_data()
        pano_view_queryset_new = context_data['object_list'].values('pk', 'title', 'view', 'latitude', 'longitude',
                                                                    'height',
                                                                    'pano_type')
        pano_view_list = list(pano_view_queryset_new)
        # Edit view field to make it URL
        for item in pano_view_list:
            item['view'] = mediapath_filter(item['view'])
        pano_view_dict = {view['pk']: view for view in pano_view_list}
        context_data['pano_view_dict'] = json.dumps(pano_view_dict)
        context_data['GOOGLE_MAPS_KEY'] = GOOGLE_MAPS_KEY
        return context_data


class FigureMapDetailView(LoginRequiredWithChoiceMixin, DetailView):
    model = FigureMap

    def get_context_data(self, **kwargs):
        update_last_activity(self.request.user)
        context_data = super().get_context_data()
        context_data['GOOGLE_MAPS_KEY'] = GOOGLE_MAPS_KEY
        return context_data


class FigureMapListView(LoginRequiredMixin, ListView):
    model = FigureMap
    ordering = ['-pk']
