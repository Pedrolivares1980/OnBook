from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserProfileForm, UserForm
from rent.models import Rental
from django.db.models import Q
from messaging.models import ChatMessage

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

# User profile editing view
@login_required
def edit_profile(request):
    # Handling profile edit requests
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
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
    return render(request, 'users/Admin_users.html', context)

# User detail view for admin
@staff_member_required
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # Add logic to retrieve user's rental history if needed
    context = {
        'user': user,
        # Add additional context for rental history
    }
    return render(request, 'users/User_detail.html', context)

# View for editing a user by admin
@staff_member_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_detail', user_id=user_id)
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user.profile)
    return render(request, 'users/edit_user.html', {'user_form': user_form, 'profile_form': profile_form, 'user': user})

# View for deleting a user by admin
@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect('admin_users')
    return render(request, 'users/delete_user.html', {'user': user})
