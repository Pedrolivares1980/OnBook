from .models import ChatMessage

# Define a function to count unread messages
def unread_messages_count(request):
    # Check if the user making the request is authenticated
    if request.user.is_authenticated:
        # Query the ChatMessage model to count messages where the current user is the receiver and the message is unread
        count = ChatMessage.objects.filter(receiver=request.user, is_read=False).count()
        # Return a dictionary with the count of unread messages
        return {'unread_messages_count': count}
    # If the user is not authenticated, return an empty dictionary
    return {}