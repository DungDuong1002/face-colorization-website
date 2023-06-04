from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from . import convert_image

# Create your models here.
class BlackWhiteImage(models.Model):
    bw_img = models.ImageField(upload_to='uploads/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now_add=True)
    output_image = models.ImageField(upload_to='converted/', blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if self.output_image is None:
            output_image = convert_image.convert_image(self.bw_img)
            buffer = BytesIO()
            output_image.save(buffer, format='JPEG')
            self.output_image.save(self.bw_img.name,
                                   InMemoryUploadedFile(buffer, None, self.bw_img.name, 'image/jpeg', buffer.getbuffer().nbytes, None))
        super().save(*args, **kwargs)
