from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:book_id>/rent/', views.rent_book, name='rent_book'),
    path('return/<int:rental_id>/', views.return_book, name='return_book'),
]