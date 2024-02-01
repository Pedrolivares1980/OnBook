from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:user_id>/', views.conversation, name='conversation'),
    path('send_message/<int:user_id>/', views.send_message, name='send_message'),
    path('start_conversation/', views.start_conversation, name='start_conversation'),
    path('delete_conversation/<int:user_id>/', views.delete_conversation, name='delete_conversation'),
]

