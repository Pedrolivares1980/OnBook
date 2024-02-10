from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='books_home'),
    path('about/', views.about, name='books_about'),
    path('books/list/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/add/', views.BookCreateView.as_view(), name='book_add'),
    path('books/update/<int:pk>/', views.BookUpdateView.as_view(), name='book_update'),
    path('books/delete/<int:pk>/', views.BookDeleteView.as_view(), name='book_delete'),
    path('books/admin/', views.BookAdminView.as_view(), name='book_admin'),
]

