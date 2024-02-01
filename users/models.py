from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.storage import default_storage as storage
from io import BytesIO

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # This method is overridden to save the profile picture and resize it if necessary.
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Open the image using the Django's storage system
        if self.image:
            img_read = storage.open(self.image.name, 'rb')
            img = Image.open(img_read)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)

                # Save the modified image to a BytesIO object
                in_mem_file = BytesIO()
                img.save(in_mem_file, format='JPEG')
                img_read.close()

                # Save the modified image back to storage
                img_write = storage.open(self.image.name, 'wb+')
                img_write.write(in_mem_file.getvalue())
                img_write.close()
