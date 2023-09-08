from django.core.exceptions import ValidationError


def get_path_upload_photo(instance, file):
    """Путь к файлу, format: (media)/profile_photos/user_id/photo.jpg
    """
    return f'profile_photos/{file}'


def validate_size_image(file_obj):
    """ Проверка размера файла
    """
    megabyte_limit = 2
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Maximum file size {megabyte_limit}MB")
