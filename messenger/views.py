from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, DetailView
from django.db.models import Count
from django.urls import reverse
from .models import Chat, Message
from authentication.models import Profile

class ChatView(TemplateView):
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chat_list"] = Chat.objects.filter(profiles=self.request.user.profile)
        return context
    
class ChatDetailView(DetailView):
    model = Chat
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chat_list"] = Chat.objects.filter(profiles=self.request.user.profile)
        return context

class MessageCreateView(CreateView):
    model = Message
    template_name = "message_create.html"
    fields = ['author', 'chat', 'content']


    def get_success_url(self):
        return reverse('chat', kwargs={'pk':self.object.chat.pk})

def get_chat(request):
    if request.method == 'GET':
        profile1 = request.user.profile
        profile2 = Profile.objects.get(pk=request.GET['profile'])
        chats = Chat.objects.annotate(
            profiles_count = Count('profiles')
        ).filter(
            profiles=profile1
        ).filter(
            profiles=profile2
        ).filter(
            profiles_count=2
        )

        if len(chats) == 0:
            chat = Chat.objects.create()
            chat.profiles.add(profile1)
            chat.profiles.add(profile2)
            chat.save()
            return redirect('chat', pk=chat.pk)
        else:
            chat = chats[0]
            return redirect('chat', pk=chat.pk)


"""
def create_message(request):
    content = request.POST.get("content")
    chat = Chat.objects.get(pk=request.POST.get("chat"))

    if content:
        Message.objects.create(author=request.user.profile, content=content, chat=chat)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=200)


async def stream_chat_messages(request, pk):
    async def event_stream():
        async for message in get_existing_messages():
            yield message

        last_id = await get_last_message_id()

        while True:
            new_messages = Message.objects.filter(chat=pk).filter(id__gt=last_id).order_by('created').values(
                'id', 'author__user__username', 'content', 'created'
            )
            async for message in new_messages:
                message['created'] = message['created'].strftime("%d/%m %H:%M")
                yield f"data: {json.dumps(message, default=str)}\n\n"
                last_id = message['id']
            await asyncio.sleep(0.1) 

    async def get_existing_messages():
        messages = Message.objects.filter(chat=pk).order_by('created').values(
            'id', 'author__user__username', 'content', 'created'
        )
        async for message in messages:
            message['created'] = make_naive(message['created']).strftime("%d/%m %H:%M")
            yield f"data: {json.dumps(message, default=str)}\n\n"

    async def get_last_message_id() -> int:
        last_message = await Message.objects.all().alast()
        return last_message.id if last_message else 0

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
"""


