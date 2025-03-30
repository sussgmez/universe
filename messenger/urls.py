from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('chat/', login_required(views.ChatView.as_view()), name='chat'),
    path('chat/<int:pk>', login_required(views.ChatDetailView.as_view()), name='chat'),
    path('messsage/create/', login_required(views.MessageCreateView.as_view()), name='message-create'),
    path('chat/get/', views.get_chat, name='get-chat'),
    path('create-message/', views.create_message, name='create-message'),
    path('stream-chat-messages/<int:pk>', views.stream_chat_messages, name='stream-chat-messages'),

]
