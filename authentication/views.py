from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Q, Count
from datetime import timedelta
from .models import Profile
from .tokens import generate_token
from .forms import SignUpForm, ProfileUpdateForm
from publications.models import Category

   
class SingUpView(View):
    template_name = "signup.html"
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


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_profile_update"] = ProfileUpdateForm 
        min_date = date.today() - timedelta(days= 2)
        context["categories"] = Category.objects.annotate(trend=Count("publication", filter=Q(publication__created__gte=min_date))).order_by('-trend')
        return context
    

class ProfileSearchListView(ListView):
    model = Profile
    template_name = "profile_list.html"
    paginate_by = 1

    def get_queryset(self):
        profiles = Profile.objects.filter(Q(user__first_name__contains=self.request.GET['text']) | Q(user__last_name__contains=self.request.GET['text']) | Q(user__username__contains=self.request.GET['text']))
        return profiles
    

class ProfileUpdateView(View):
    template_name = "profile_update.html"
    form_class = ProfileUpdateForm

    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.update(request, pk)
            return redirect('profile', pk)
        else:
            return render(request, self.template_name, {'form':form})


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

