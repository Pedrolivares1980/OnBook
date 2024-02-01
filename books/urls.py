from django.urls import path
from . import views

urlpatterns = [
    # URL para la página principal de libros
    path('', views.home, name='books_home'),

    # URL para la página 'about' de libros
    path('about/', views.about, name='books_about'),

    # URL para listar todos los libros
    path('books/list/', views.BookListView.as_view(), name='book_list'),

    # URL para ver detalles de un libro específico
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),

    # URL para agregar un nuevo libro
    path('books/add/', views.BookCreateView.as_view(), name='book_add'),

    # URL para actualizar un libro
    path('books/update/<int:pk>/', views.BookUpdateView.as_view(), name='book_update'),

    # URL para eliminar un libro
    path('books/delete/<int:pk>/', views.BookDeleteView.as_view(), name='book_delete'),

    # URL para la administración de libros (por un usuario del staff)
    path('books/admin/', views.BookAdminView.as_view(), name='book_admin'),
]

