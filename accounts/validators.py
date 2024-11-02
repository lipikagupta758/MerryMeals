from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    ext= os.path.splitext(value.name)[1]
    valid_extensions= ['.jpg', '.png', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions are: '+ str(valid_extensions))