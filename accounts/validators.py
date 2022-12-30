# File for validation purposes and functions
from django.core.exceptions import ValidationError
import os 


def allow_only_images_validator(value):
    # Value is just a filename we are uploading
    ext = os.path.splitext(value.name)[1] #image.jpg [1] position is an file extension in this case it's "jpg"
    valid_extensions = ['.png', '.jpg', '.jpeg',]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed file extensions are: '+ str(valid_extensions))
