from django.core.management import BaseCommand

from unique_content.models import LinkSpotCoordinates
from unique_content.services import haversine


class Command(BaseCommand):
    def handle(self, *args, **options):
        links_queryset = LinkSpotCoordinates.objects.all()
        for item in links_queryset:
            if item.panorama_from.latitude and item.panorama_from.longitude and item.panorama_to.latitude and item.panorama_to.longitude:
                pano_from = item.panorama_from
                pano_to = item.panorama_to
                item.distance = haversine(pano_from.latitude, pano_from.longitude, pano_to.latitude, pano_to.longitude,
                                          pano_from.height, pano_to.height)
                item.save()
