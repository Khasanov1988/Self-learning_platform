from django.core.management import BaseCommand

from unique_content.models import InfoSpotCoordinates
from unique_content.services import haversine


class Command(BaseCommand):
    def handle(self, *args, **options):
        info_spot_queryset = InfoSpotCoordinates.objects.all()
        for item in info_spot_queryset:
            if item.panorama.latitude and item.panorama.longitude and item.info_spot.latitude and item.info_spot.longitude:
                pano = item.panorama
                info_sp = item.info_spot
                item.distance = haversine(pano.latitude, pano.longitude, info_sp.latitude, info_sp.longitude,
                                          pano.height, info_sp.height)
                item.save()
