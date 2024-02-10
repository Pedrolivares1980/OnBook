from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserProfileForm, UserForm
from rent.models import Rental
from django.db.models import Q
from messaging.models import ChatMessage
from .models import Profile
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully, now you can login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# User profile view
@login_required
def profile(request):
    # Updating user and profile information
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Retrieving unreaded messages
    unread_messages = ChatMessage.objects.filter(receiver=request.user, is_read=False)

    # Retrieving user's rental history
    current_rentals = Rental.objects.filter(user=request.user, actual_return_date__isnull=True)
    past_rentals = Rental.objects.filter(user=request.user, actual_return_date__isnull=False)

    context = {
        "u_form": u_form, 
        "p_form": p_form,
        "current_rentals": current_rentals,
        "past_rentals": past_rentals,
        "unread_messages": unread_messages,
    }

    return render(request, "users/profile.html", context)

@login_required
def edit_profile(request, user_id=None):
    if user_id and not request.user.is_staff:
        messages.error(request, "You are not authorized to edit this profile.")
        return redirect('home')  

    user = get_object_or_404(User, pk=user_id) if user_id else request.user

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile has been updated!')
            return redirect('user_detail', user_id=user.pk) 
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': user
    }

    return render(request, 'users/edit_profile.html', context)

# View for admin to see all users
@staff_member_required
def UserAdminView(request):
    # Filtering users based on query
    queryset = User.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(Q(username__icontains=query) | Q(email__icontains=query))

    context = {
        'users': queryset,
    }
    return render(request, 'users/admin_users.html', context)

# User detail view for admin
@staff_member_required
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # Retrieving user's rental history
    current_rentals = Rental.objects.filter(user=user, actual_return_date__isnull=True)
    past_rentals = Rental.objects.filter(user=user, actual_return_date__isnull=False)

    context = {
        'user': user,
        'current_rentals': current_rentals,
        'past_rentals': past_rentals,

    }
    return render(request, 'users/user_detail.html', context)



# View for deleting a user by admin or user
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.user.is_staff or request.user == user:
        if request.method == "POST":
            user.delete()
            messages.success(request, 'The user account has been successfully deleted.')
            if request.user.is_staff:
                return redirect('admin_users')
            else:
                return redirect('home')
        return render(request, 'users/delete_user.html', {'user': user})
    else:
        messages.error(request, 'You do not have permission to delete this user.')
        return redirect('home')

@login_required
def download_user_data(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    profile = Profile.objects.get(user=request.user)

    p.drawString(100, 800, "User Information")
    p.drawString(100, 780, f"Username: {request.user.username}")
    p.drawString(100, 760, f"Email: {request.user.email}")

    rentals = Rental.objects.filter(user=request.user)
    y_position = 720 
    for rental in rentals:
        p.drawString(100, y_position, f"Book: {rental.book.name}, Rental Date: {rental.rental_date.strftime('%d-%m-%Y')}")
        y_position -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='user_data.pdf')