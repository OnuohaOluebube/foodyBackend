from django.core.exceptions import ValidationError
def validate_file_size(file):
    max_file_size_kb = 50

    if file.size > max_file_size_kb:
        raise ValidationError(f'Files cannot be larger than {max_file_size_kb}KB!')
