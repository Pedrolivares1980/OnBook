from django.db import models
from django.contrib.auth.models import User
from PIL import Image, UnidentifiedImageError
from django.core.files.storage import default_storage as storage
from io import BytesIO

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            try:
                # Open the image using Django's storage system
                with storage.open(self.image.name, 'rb') as img_read:
                    img = Image.open(img_read)

                    # Correct image orientation
                    if hasattr(img, '_getexif'):
                        exif = img._getexif()
                        if exif:
                            orientation = exif.get(0x0112)
                            if orientation == 3:
                                img = img.rotate(180, expand=True)
                            elif orientation == 6:
                                img = img.rotate(270, expand=True)
                            elif orientation == 8:
                                img = img.rotate(90, expand=True)

                    # Resize the image
                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)

                        # Save the modified image to a BytesIO object
                        in_mem_file = BytesIO()
                        img.save(in_mem_file, format='JPEG')
                        in_mem_file.seek(0)

                        # Save the modified image back to storage
                        with storage.open(self.image.name, 'wb+') as img_write:
                            img_write.write(in_mem_file.getvalue())
            except UnidentifiedImageError:
                # Handle the case where the file is not a valid image
                print(f'Error processing image for user {self.user.username}: File is not a valid image.')
            except Exception as e:
                # Handle any other exceptions
                print(f'Unexpected error processing image for user {self.user.username}: {e}')

