import math
from io import BytesIO

from PIL import Image
from PIL.ExifTags import TAGS
from django.core.files.storage import default_storage
from django.utils import timezone

import numpy as np


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


def image_compression(image_field, quality: int, new_size: dict = None):
    """
    Compresses the given image with the specified quality and returns the compressed image.
    Optionally resizes the image by the given percentage.
    """
    # Opening an image using Pillow
    image = Image.open(image_field)
    # Creating a Buffer for a Compressed Image
    compressed_img_buffer = BytesIO()

    # Compressing an image and saving it to a buffer
    img = image.copy()
    if new_size:
        # Calculate new image dimensions
        width, height = img.size
        new_width = int(new_size['width'])
        new_height = int(new_size['height'])

        # Resize Image
        img = img.resize((new_width, new_height), Image.LANCZOS)

    # Compressing an image and saving it to a buffer
    img.save(compressed_img_buffer, format=image.format, quality=quality)

    return compressed_img_buffer


def get_youtube_for_iframe_from_youtube(youtube: str):
    """
        Function transfer YouTube link to YouTube link for InfoSpot iframe
    """
    video_id = youtube.split('v=')[1]
    return f'https://www.youtube.com/embed/{video_id}?&amp;autoplay=1&mute=1&disablekb=1&loop=1&playlist={video_id}&controls=0&iv_load_policy=3'


def north_correction(panorama, info_point_coords, info_point_list):
    angles = []
    # Исходные данные
    main_latitude = panorama.latitude
    main_longitude = panorama.longitude
    info_points = []

    # Перевод географических координат в декартовы
    main_X = np.cos(np.radians(main_latitude)) * np.cos(np.radians(main_longitude))
    main_Y = np.cos(np.radians(main_latitude)) * np.sin(np.radians(main_longitude))
    main_Z = np.sin(np.radians(main_latitude))
    kopt = np.array([main_X, main_Y, main_Z])

    # Вычисление угла между севером и направлением на точку от коптера - alfa
    sever = np.array([0, 0, 1])  # Координаты севера в декартовой системе
    vector_north = sever - kopt

    info_point_coord_list = list(info_point_coords)

    for info_point_coord in info_point_coord_list:
        if info_point_coord.is_reference:
            object_info_point = info_point_list.get(pk=info_point_coord.info_spot.pk)
            X = np.cos(np.radians(object_info_point.latitude)) * np.cos(
                np.radians(object_info_point.longitude))
            Y = np.cos(np.radians(object_info_point.latitude)) * np.sin(
                np.radians(object_info_point.longitude))
            Z = np.sin(np.radians(object_info_point.latitude))
            info_point_vector = np.array([X, Y, Z]) - kopt
            alfa = np.degrees(np.arccos(np.dot(vector_north, info_point_vector) / (
                    np.linalg.norm(vector_north) * np.linalg.norm(info_point_vector))))
            if main_longitude > object_info_point.longitude:
                alfa = 360 - alfa
            betta = np.degrees(np.arccos(info_point_coord.coord_Z / np.sqrt(5000 ** 2 - info_point_coord.coord_Y ** 2)))
            if info_point_coord.coord_X < 0:
                betta = 360 - betta

            correction_angle = (alfa - betta + 360) % 360

            info_points.append(info_point_coord)
            angles.append(correction_angle)
            info_point_coord.correction_angle = correction_angle
            info_point_coord.save()

    # Сортировка данных
    sorted_data = sorted(angles)

    # Находим медианное значение
    mid = len(sorted_data) // 2
    if len(sorted_data) % 2 == 0:
        median = (sorted_data[mid - 1] + sorted_data[mid]) / 2
    else:
        median = sorted_data[mid]

    panorama.north_correction_angle = 180 - median
    panorama.save()


def clean_old_data_for_view_field(instance, model_class):
    if instance.pk:  # Check if object has been saved previously
        try:
            old_instance = model_class.objects.get(pk=instance.pk)
            if old_instance.view and instance.view != old_instance.view:
                default_storage.delete(old_instance.view.name)
            if old_instance.preview:
                default_storage.delete(old_instance.preview.name)
        except model_class.DoesNotExist:
            pass


def haversine(lat1, lon1, lat2, lon2, elev1=0, elev2=0):
    """ Calculation distance between 2 points on Earth"""
    # Радиус Земли в километрах
    R = 6371

    # Преобразование градусов в радианы
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Вычисление разницы между широтами и долготами
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Вычисление расстояния с помощью формулы Гаверсинуса
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    elevation = abs(elev2 - elev1)/1000

    # Учет высоты над уровнем моря
    abs_distance = math.sqrt(distance**2 + elevation**2)

    return abs_distance * 1000
