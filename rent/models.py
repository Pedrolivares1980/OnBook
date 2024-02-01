from django.db import models
from django.contrib.auth.models import User
from books.models import Book

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rental_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)  # Fecha planeada de devolución
    actual_return_date = models.DateField(null=True, blank=True)  # Fecha real de devolución


    def __str__(self):
        return f"{self.book.name} alquilado por {self.user.username}"

