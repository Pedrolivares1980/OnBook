from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatMessage
from .forms import MessageForm
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def inbox(request):
    """
    Display the inbox with a list of users who have had conversations with the current user.
    """
    all_users = User.objects.exclude(id=request.user.id)
    users_with_conv = User.objects.filter(
        Q(sent_messages__receiver=request.user) | 
        Q(received_messages__sender=request.user)
    ).distinct().exclude(id=request.user.id)

    # Get all unread messages for the current user
    unread_messages = ChatMessage.objects.filter(receiver=request.user, is_read=False)

    return render(request, 'messaging/inbox.html', {
        'users_with_conv': users_with_conv, 
        'all_users': all_users,
        'unread_messages': unread_messages
    })

@login_required
def start_conversation(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        recipient = get_object_or_404(User, id=recipient_id)

        # Redirect to the conversation view with the selected user
        return redirect('send_message', user_id=recipient.id)
    else:
        # If not a POST request, redirect back to the inbox
        return redirect('inbox')


@login_required
def conversation(request, user_id):
    """
    Display a conversation between the current user and the selected user.
    """
    other_user = get_object_or_404(User, id=user_id)
    chat_messages = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) | 
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')
    return render(request, 'messaging/conversation.html', {'chat_messages': chat_messages, 'other_user': other_user})

@login_required
def send_message(request, user_id):
    """
    Send a new message to another user.
    """
    receiver = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.sender = request.user
            chat_message.receiver = receiver
            chat_message.save()
            return redirect('conversation', user_id=user_id)
    else:
        form = MessageForm()
    return render(request, 'messaging/send_message.html', {'form': form, 'receiver': receiver})

@login_required
def delete_conversation(request, user_id):
    """
    Delete all messages in a conversation with another user.
    """
    other_user = get_object_or_404(User, id=user_id)
    
    # Ensure that the request.user is part of the conversation
    if request.user == other_user:
        messages.error(request, "You cannot delete a conversation with yourself.")
        return redirect('inbox')

    ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).delete()

    messages.success(request, "The conversation has been deleted.")
    return HttpResponseRedirect(reverse('inbox'))
