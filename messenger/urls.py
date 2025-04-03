from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('chat/', login_required(views.ChatView.as_view()), name='chat'),
    path('chat/<int:pk>', login_required(views.ChatDetailView.as_view()), name='chat'),
    path('chat/get/', views.get_chat, name='get-chat'),
    path('messsage/create/', login_required(views.MessageCreateView.as_view()), name='message-create'),
]
