from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    """
    Model for messages in the messaging app.
    Each message has a sender, receiver, content, and timestamp.
    """
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    replied_to = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} - {self.timestamp.strftime("%Y-%m-%d %H:%M")}'
