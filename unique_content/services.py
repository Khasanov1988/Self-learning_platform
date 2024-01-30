from PIL import Image
from PIL.ExifTags import TAGS
from django.utils import timezone


def get_metadata_from_img(path):
    """
    Function get latitude, longitude, height and image_creation_date metadata from JPG file
    """
    image_creation_date = latitude = longitude = height = None

    # Open the image file
    image = Image.open(path)
    print(image)

    # Get EXIF data
    exif_data = image._getexif()
    if exif_data:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag)
            if tag_name == 'DateTimeOriginal':
                image_creation_date = timezone.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                break

    # Get GPS data
    gps_info = exif_data.get(34853) if exif_data else None
    if gps_info:
        # Extract latitude, longitude, and height
        latitude_ref = gps_info.get(1)
        latitude = gps_info.get(2)
        longitude_ref = gps_info.get(3)
        longitude = gps_info.get(4)
        if latitude and longitude:
            latitude = latitude[0] + latitude[1] / 60 + latitude[2] / 3600
            longitude = longitude[0] + longitude[1] / 60 + longitude[2] / 3600
            if latitude_ref == 'S':
                latitude = -latitude
            if longitude_ref == 'W':
                longitude = -longitude
            latitude = latitude
            longitude = longitude
        # Extract height if available
        altitude = gps_info.get(6)
        if altitude:
            height = float(altitude)

    return image_creation_date, latitude, longitude, height
