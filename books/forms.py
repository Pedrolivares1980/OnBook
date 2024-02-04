from django import forms
from django.forms import DateInput
from .models import Book
from django.utils import timezone
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from django.core.files import File
from django.core.exceptions import ValidationError
import logging


# Set up logging, with an appropriate name and level
logger = logging.getLogger(__name__)


class BookForm(forms.ModelForm):
    """Form for Book model with custom validations."""

    class Meta:
        model = Book
        fields = [
            "name",
            "author",
            "publisher",
            "publish_date",
            "language",
            "cover_image",
            "category",
            "description",
            "is_available",
        ]
        widgets = {
            "publish_date": DateInput(attrs={"type": "date"}, format="%d/%m/%Y"),
        }
        help_texts = {
            "name": "Enter the full title of the book.",
            "author": "Name of the author or authors.",
            "publisher": "Enter the name of the publisher company",
            "category": "Select the most fitting category for the book.",
            "description": "Enter  a brief description about this book.",
        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields["publish_date"].input_formats = ["%d/%m/%Y", "%Y-%m-%d"]

    def clean_publish_date(self):
        """Ensure publish date is not in the future."""
        publish_date = self.cleaned_data.get("publish_date")
        if publish_date and publish_date > timezone.now().date():
            raise forms.ValidationError("Publish date cannot be in the future.")
        return publish_date

    def save(self, commit=True):
        """Save the model instance with the option to process the cover image before saving."""
        book = super().save(commit=False)

        if "cover_image" in self.changed_data:
            cover_image = self.cleaned_data.get("cover_image")

            if cover_image:  # Check if an image was uploaded
                try:
                    img = Image.open(cover_image)
                    # Correct the orientation of the image based on EXIF data
                    img = self.correct_image_orientation(img)
                    # Resize the image if necessary
                    img = self.resize_image(img, max_size=(600, 600))

                    # Save the processed image to a BytesIO buffer
                    in_mem_file = BytesIO()
                    img.save(in_mem_file, format="JPEG")
                    in_mem_file.seek(0)
                    # Save the image to the model's cover_image field
                    book.cover_image.save(
                        cover_image.name, content=File(in_mem_file), save=False
                    )
                except UnidentifiedImageError:
                    # Log the error for developer's debugging purposes
                    logger.error(
                        f"UnidentifiedImageError: The image {cover_image.name} could not be processed."
                    )

                    # Add an error message to the form to inform the user with the 'error' message tag
                    self.add_error(
                        "cover_image",
                        ValidationError(
                            "The uploaded image could not be processed. Please try again with a different image.",
                            code="invalid",
                            params={"value": self.cleaned_data["cover_image"]},
                            message="error",
                        ),
                    )

        if commit:
            book.save()  # Save the book instance to the database
            self._save_m2m()  # Save many-to-many relations

        return book

    def correct_image_orientation(self, img):
        """Correct the orientation of an image using EXIF data."""
        if hasattr(img, "_getexif"):
            exif = img._getexif()
            if exif:
                orientation = exif.get(0x0112)
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)
        return img

    def resize_image(self, img, max_size=(600, 600)):
        """Resize an image to fit within a specified size."""
        if img.height > max_size[1] or img.width > max_size[0]:
            img.thumbnail(max_size)  # Resize the image in-place
        return img
