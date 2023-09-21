from django.core.exceptions import ValidationError, ObjectDoesNotExist

from src.search.models import Favorites


def get_path_upload_photo(instance, file):
    """Путь к файлу, format: (media)/profile_photos/user_id/photo.jpg"""
    return f"profile_photos/{file}"


def validate_size_image(file_obj):
    """Проверка размера файла"""
    megabyte_limit = 7
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Maximum file size {megabyte_limit}MB")


def get_isfavorite(user, tourid):
    try:
        Favorites.objects.get(user=user, tourid=tourid)
        return True
    except ObjectDoesNotExist:
        return False
