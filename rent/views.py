from django.shortcuts import get_object_or_404, redirect, render
from .models import Rental
from books.models import Book
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

def rent_book(request, book_id):
    """
    View to handle book rental.
    """
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        # Create a new rental record
        rental = Rental(
            user=request.user,
            book=book,
            return_date=timezone.now() + timedelta(days=30)  # Set return date 30 days from now
        )
        rental.save()

        # Update book availability if needed
        book.is_available = False
        book.save()

        messages.success(request, 'You have successfully rented the book.')
        return redirect('profile')

    # Render a confirmation page before renting
    return render(request, 'rent/rent_confirmation.html', {'book': book})

def return_book(request, rental_id):
    # Obtén el alquiler basado en el ID y verifica que pertenezca al usuario y que aún no haya sido devuelto
    rental = get_object_or_404(Rental, id=rental_id, user=request.user, actual_return_date__isnull=True)

    # Marca el libro como devuelto actualizando el campo 'actual_return_date'
    rental.actual_return_date = timezone.now()
    rental.save()

    # Actualiza la disponibilidad del libro si es necesario
    # Suponiendo que hay un campo 'is_available' en el modelo Book
    rental.book.is_available = True
    rental.book.save()

    messages.success(request, 'You have successfully returned the book.')
    return redirect('profile')
