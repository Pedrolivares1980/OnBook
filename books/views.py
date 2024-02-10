from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
import random
from .models import Book
from rent.models import Rental
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from .forms import BookForm

class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin to restrict access to staff members only."""
    def test_func(self):
        return self.request.user.is_staff

class BookMixin:
    """Mixin to add common context data used in multiple book views."""
    def get_common_context(self, context):
        context['authors'] = Book.objects.values_list('author', flat=True).distinct()
        context['publishers'] = Book.objects.values_list('publisher', flat=True).distinct()
        context['categories'] = dict(Book.CATEGORY_CHOICES)
        return context

def home(request):
    """Home view to display random selection of books with cover images."""
    books_with_covers = Book.objects.exclude(cover_image='').all()
    random_books = random.sample(list(books_with_covers), min(len(books_with_covers), 6))
    context = {'random_books': random_books}
    return render(request, 'books/home.html', context)

def about(request):
    """About view to display information about the application."""
    return render(request, 'books/about.html')

class BookListView(BookMixin, ListView):
    """View for listing books with filters."""
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 9

    def get_queryset(self):
        """Modify the queryset based on search and filter criteria."""
        queryset = Book.objects.all()
        query = self.request.GET.get('q')
        filter_by_author = self.request.GET.get('author')
        filter_by_publisher = self.request.GET.get('publisher')
        filter_by_category = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if filter_by_author:
            queryset = queryset.filter(author__icontains=filter_by_author)
        if filter_by_publisher:
            queryset = queryset.filter(publisher__icontains=filter_by_publisher)
        if filter_by_category:
            queryset = queryset.filter(category__icontains=filter_by_category)

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        """Add common context data to the context."""
        context = super().get_context_data(**kwargs)
        return self.get_common_context(context)

class BookDetailView(DetailView):
    """View for displaying book details."""
    model = Book
    template_name = 'books/book_detail.html'

    def post(self, request, *args, **kwargs):
        """Handle POST requests for book rentals."""
        book = self.get_object()
        Rental.objects.create(user=request.user, book=book, return_date=timezone.now() + timezone.timedelta(days=14))
        messages.success(request, 'You have successfully rented the book.')
        return redirect('book_detail', pk=book.pk)

class BookCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """View for creating a new book."""
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_admin')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Book added successfully.')
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)

class BookUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """View for updating a book."""
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'

    def get_success_url(self):
        """Redirect to book detail page after successful update."""
        return reverse('book_admin')


    def form_valid(self, form):
        """Handle form submission."""
        messages.success(self.request, 'Book updated successfully.')
        return super().form_valid(form)

class BookDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """View for deleting a book."""
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('book_admin')

class BookAdminView(BookMixin, LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Admin view for managing books."""
    model = Book
    template_name = 'books/book_admin.html'
    context_object_name = 'books'
    paginate_by = 5

    def test_func(self):
        """Restrict this view to staff users only."""
        return self.request.user.is_staff

    def get_queryset(self):
        """Modify the queryset based on admin-specific filters."""
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(author__icontains=query) | Q(publisher__icontains=query))

        filter_by_author = self.request.GET.get('author')
        if filter_by_author:
            queryset = queryset.filter(author__icontains=filter_by_author)

        filter_by_publisher = self.request.GET.get('publisher')
        if filter_by_publisher:
            queryset = queryset.filter(publisher__icontains=filter_by_publisher)

        filter_by_category = self.request.GET.get('category')
        if filter_by_category:
            queryset = queryset.filter(category=filter_by_category)

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        """Add common context data to the context."""
        context = super().get_context_data(**kwargs)
        return self.get_common_context(context)
