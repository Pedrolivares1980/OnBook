from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    replied_to = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} - {self.timestamp.strftime("%d-%m-%Y %H:%M")}'
