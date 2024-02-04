from django.db import models


class Book(models.Model):
    CATEGORY_CHOICES = [
        ("novel", "Novel"),
        ("fiction", "Fiction"),
        ("non_fiction", "Non-Fiction"),
        ("science_fiction", "Science Fiction"),
        ("fantasy", "Fantasy"),
        ("mystery", "Mystery"),
        ("thriller", "Thriller"),
        ("horror", "Horror"),
        ("biography", "Biography"),
        ("autobiography", "Autobiography"),
        ("history", "History"),
        ("philosophy", "Philosophy"),
        ("self_help", "Self Help"),
        ("economics", "Economics"),
        ("politics", "Politics"),
        ("science", "Science"),
        ("technology", "Technology"),
        ("art", "Art"),
        ("music", "Music"),
        ("cooking", "Cooking"),
        ("travel", "Travel"),
        ("sports", "Sports"),
        ("religion", "Religion"),
        ("education", "Education"),
        ("poetry", "Poetry"),
        ("drama", "Drama"),
        ("essay", "Essay"),
        ("children", "Children"),
        ("young_adult", "Young Adult"),
        ("health", "Health"),
        ("wellness", "Wellness"),
        ("humor", "Humor"),
        ("comics", "Comics"),
        ("romance", "Romance"),
        ("erotic", "Erotic"),
    ]

    name = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=100, null=True)
    publisher = models.CharField(max_length=100, null=True)
    publish_date = models.DateField(null=True)
    language = models.CharField(max_length=50, null=True)
    cover_image = models.ImageField(upload_to="book_covers/", blank=True, null=True)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True
    )
    description = models.TextField(null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
