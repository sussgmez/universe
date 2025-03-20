from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.contrib.auth import login, logout
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.urls import reverse
from django.http import HttpResponse
from .tokens import generate_token
from .forms import SignUpForm, PostForm, ProfileUpdateForm
from .models import Post, Profile, Category, Chat, Message


class HomeView(TemplateView):
    template_name = "social_network/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_form"] = PostForm
        context["categories"] = Category.objects.all()
        return context
    

class SearchView(TemplateView):
    template_name = "social_network/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text"] = self.request.GET['text']
        context["categories"] = Category.objects.all()
        context["category_search"] = int(self.request.GET['category'])
        return context
    

class PostCreateView(CreateView):
    model = Post
    template_name = "social_network/post_create.html"
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        return redirect('home')

    def get_success_url(self):
        try:
            return reverse('post', kwargs={'pk':self.object.commented.pk})
        except: pass
        return reverse('home')


class PostDetailView(DetailView):
    model = Post
    template_name = "social_network/post.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_form"] = PostForm
        context["categories"] = Category.objects.all()
        return context


class PostListView(ListView):
    model = Post
    template_name = "social_network/post_list.html"
    paginate_by = 10

    def get_queryset(self):
        posts = Post.objects.filter(author__in=self.request.user.profile.following.all())
        posts = posts.order_by('-created')
        return posts
    

class PostSearchListView(ListView):
    model = Post
    template_name = "social_network/post_list.html"
    paginate_by = 10

    def get_queryset(self):
        category_pk = int(self.request.GET['category'])
        if category_pk != 0:
            posts = Post.objects.filter(Q(content__contains=self.request.GET['text']) & Q(category=category_pk))
        else:
            posts = Post.objects.filter(Q(content__contains=self.request.GET['text']))
        posts = posts.order_by('-created')
        return posts
    

class PostProfileListView(ListView):
    model = Post
    template_name = "social_network/post_list.html"
    ordering = ['-created']
    paginate_by = 10

    def get_queryset(self):
        posts = Post.objects.filter(author=self.request.GET['profile'])
        posts = posts.order_by('-created')
        return posts
    

class PostCommentListView(ListView):
    model = Post
    template_name = "social_network/post_list.html"
    ordering = ['-created']
    paginate_by = 10

    def get_queryset(self):
        posts = Post.objects.filter(commented=self.request.GET['post'])
        posts = posts.order_by('-created')
        return posts


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "social_network/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_profile_update"] = ProfileUpdateForm 
        context["categories"] = Category.objects.all()
        return context
    

class ProfileSearchListView(ListView):
    model = Profile
    template_name = "social_network/profile_list.html"
    paginate_by = 5

    def get_queryset(self):
        profiles = Profile.objects.filter(Q(user__first_name__contains=self.request.GET['text']) | Q(user__last_name__contains=self.request.GET['text']) | Q(user__username__contains=self.request.GET['text']))
        return profiles
    
   
class SingUpView(View):
    template_name = "social_network/signup.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        
        form = self.form_class
        return render(request, self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.signup(request)
            messages.success(request, "Se ha enviado un correo para activar su cuenta.")
            return redirect('login')
        else:
            return render(request, self.template_name, {'form':form})


class ProfileUpdateView(View):
    template_name = "social_network/profile_update.html"
    form_class = ProfileUpdateForm

    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.update(request, pk)
            return redirect('profile', pk)
        else:
            return render(request, self.template_name, {'form':form})


class ChatView(TemplateView):
    template_name = "social_network/chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_chats"] = Chat.objects.filter(profiles=self.request.user.profile)
        return context
    

class ChatDetailView(DetailView):
    model = Chat
    template_name = "social_network/chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_chats"] = Chat.objects.filter(profiles=self.request.user.profile)
        return context
    

class MessageCreateView(CreateView):
    model = Message
    template_name = "social_network/message_create.html"
    fields = ['sender_profile', 'receiver_chat', 'content']

    def get_success_url(self):
        
        return reverse('chat', kwargs={'pk':self.object.receiver_chat.pk})




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


def activate(request):
    try:
        uidb64 = request.GET['uidb64']
        token = request.GET['token']
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, MultiValueDictKeyError):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Su cuenta ha sido activada con éxito.")
        return redirect('home')
    else:
        messages.error(request, "Error al activar cuenta.")
        return redirect('login')
 

def logout_handler(request):
    logout(request)
    return redirect('login')


def like_post(request, pk):
    if request.method == 'GET':
        post = Post.objects.get(pk=pk)
        
        if post in request.user.profile.liked_post.all():
            request.user.profile.liked_post.remove(post)
            request.user.profile.save()
            lk_post = len(Profile.objects.filter(liked_post=post))
            html = f'<p>{lk_post}</p><img src="/static/images/hearth_icon.png" alt="" srcset="">'        
        else:
            request.user.profile.liked_post.add(post)
            request.user.profile.save()
            lk_post = len(Profile.objects.filter(liked_post=post))
            html = f'<p>{lk_post}</p><img src="/static/images/hearth_icon_2.png" alt="" srcset="">'        


        return HttpResponse(html)


def delete_post(request, pk):
    if request.method == 'POST':
        Post.objects.filter(pk=pk).delete()
        return redirect('home')


def follow(request):
    if request.method == 'POST':
        profile = Profile.objects.get(pk=request.POST['following'])
        user_profile = request.user.profile
        user_profile.following.add(profile)
        user_profile.save()
        return redirect('profile', pk=profile.pk)
    else:
        return redirect('home')
    

def unfollow(request):
    if request.method == 'POST':
        profile = Profile.objects.get(pk=request.POST['following'])
        user_profile = request.user.profile
        user_profile.following.remove(profile)
        user_profile.save()
        return redirect('profile', pk=profile.pk)
    else:
        return redirect('home')
    

