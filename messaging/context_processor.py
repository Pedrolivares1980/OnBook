from django.contrib.auth.models import User
from .models import ChatMessage

def unread_messages_count(request):
    if request.user.is_authenticated:
        count = ChatMessage.objects.filter(receiver=request.user, is_read=False).count()
        return {'unread_messages_count': count}
    return {}