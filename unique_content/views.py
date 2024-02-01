import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.views.generic import DetailView, ListView

from education_content.templatetags.my_tags import mediapath_filter
from education_content.views import LoginRequiredWithChoiceMixin
from unique_content.models import FigureThinSection, FigureFromP3din, Figure360View, InfoSpotForPanorama, \
    InfoSpotCoordinates, LinkSpotCoordinates
from users.services import update_last_activity


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
        pano_view_list = list(
            Figure360View.objects.all().values('pk', 'title', 'view', 'latitude', 'longitude', 'height', 'pano_type'))
        # Edit view field to make it URL
        for item in pano_view_list:
            item['view'] = mediapath_filter(item['view'])
        pano_view_dict = {view['pk']: view for view in pano_view_list}
        info_spot_queryset = InfoSpotForPanorama.objects.all().annotate(
            figure_thin_section_preview=F('figure_thin_section__preview'),
            figure_3d_link_for_iframe=F('figure_3d__link_for_iframe'))

        info_spot_list = list(info_spot_queryset.values())
        print(info_spot_list)
        info_spot_dict = {view['id']: view for view in info_spot_list}
        info_spot_coordinates_list = list(InfoSpotCoordinates.objects.all().values())
        link_spot_coordinates_list = list(LinkSpotCoordinates.objects.all().values())
        context_data['pano_view_dict'] = json.dumps(pano_view_dict)
        context_data['info_spot_dict'] = json.dumps(info_spot_dict)
        context_data['info_spot_coordinates_list'] = json.dumps(info_spot_coordinates_list)
        context_data['link_spot_coordinates_list'] = json.dumps(link_spot_coordinates_list)
        return context_data


class Figure360ViewListView(LoginRequiredMixin, ListView):
    model = Figure360View
    ordering = ['-pk']
