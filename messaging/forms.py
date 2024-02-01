from django import forms
from .models import ChatMessage

class MessageForm(forms.ModelForm):
    """
    Form for creating a message.
    """
    class Meta:
        model = ChatMessage
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your message here...'})
