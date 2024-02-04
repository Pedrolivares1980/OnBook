from django import forms
from django.forms import DateInput
from .models import Book
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files import File

class BookForm(forms.ModelForm):
    """Form for Book model with custom validations."""

    class Meta:
        model = Book
        fields = ['name', 'author', 'publisher', 'publish_date', 'language', 'cover_image', 'category', 'description', 'is_available']
        widgets = {
            'publish_date': DateInput(attrs={'type': 'date'}, format='%d/%m/%Y'),
        }
        help_texts = {
            'name': 'Enter the full title of the book.',
            'author': 'Name of the author or authors.',
            'publisher': 'Enter the name of the publisher company',
            'category': 'Select the most fitting category for the book.',
            'description': 'Enter  a brief description about this book.',
        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['publish_date'].input_formats = ('%d/%m/%Y',)

    def clean_publish_date(self):
        """Ensure publish date is not in the future."""
        publish_date = self.cleaned_data.get('publish_date')
        if publish_date and publish_date > timezone.now().date():
            raise forms.ValidationError("Publish date cannot be in the future.")
        return publish_date

    def save(self, commit=True):
        """Process the book cover image before saving."""
        book = super().save(commit=False)
        
        if 'cover_image' in self.changed_data:
            cover_image = self.cleaned_data.get('cover_image')
            
            if cover_image:  # Check if an image was uploaded
                # Open the image and Correct image orientation
                img = Image.open(cover_image)
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
                # Open the image and resize it
                if img.height > 600 or img.width > 600:
                    output_size = (600, 600)
                    img.thumbnail(output_size)
                    in_mem_file = BytesIO()
                    img.save(in_mem_file, format='JPEG')
                    in_mem_file.seek(0)
                    book.cover_image.save(cover_image.name, content=File(in_mem_file), save=False)
        
        if commit:
            book.save()
            self._save_m2m()
        
        return book
