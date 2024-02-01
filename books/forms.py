from django import forms
from .models import Book
from django.utils import timezone

class BookForm(forms.ModelForm):
    """Form for Book model with custom validations."""
    cover_image = forms.URLField(help_text="Enter the URL of the book cover image.")
    class Meta:
        model = Book
        fields = ['name', 'author', 'publisher', 'publish_date', 'language', 'cover_image', 'category', 'description', 'is_available']
        
    def clean_publish_date(self):
        publish_date = self.cleaned_data.get('publish_date')
        if publish_date and publish_date > timezone.now().date():
            raise forms.ValidationError("Publish date cannot be in the future.")
        return publish_date
