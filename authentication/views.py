import secrets
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.mail import send_mail
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Count
from datetime import date, timedelta
from publications.models import Category
from .models import Profile
from .forms import ActivateForm, ProfileUpdateForm, SignUpForm, LoginForm


class LoginView(TemplateView):
    """
    Vista de inicio de sesión:
        - Cuenta con manejo de errores de inicio de sesión. 
        - Solo los usuarios registrados por la universidad pueden hacer uso de la red social.
    """
    template_name = 'login.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = LoginForm()
        return context
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('home')
        else:
            return render(request, self.template_name, {'form':form})     
              
    
class ActivateView(View):
    """
    Vista de activación de cuentas. Solo los usuarios registrados por la universidad pueden activar su cuenta.
    """
    template_name = "activate.html"
    form_class = ActivateForm
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        
        form = self.form_class
        return render(request, self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.activate(request)
            messages.success(request, "Usuario activado correctamente.")
            return redirect('login')
        else:
            return render(request, self.template_name, {'form':form})


class ProfileDetailView(DetailView):
    """
    Vista de perfil de usuario.
    """
    model = Profile
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_profile_update"] = ProfileUpdateForm 
        min_date = date.today() - timedelta(days= 2)
        context["categories"] = Category.objects.annotate(trend=Count("publication", filter=Q(publication__created__gte=min_date))).order_by('-trend')
        return context
    

class ProfileSearchListView(ListView):
    """
    Vista externa para buscar perfiles de usuarios.
    """
    model = Profile
    template_name = "profile_list.html"
    paginate_by = 5

    def get_queryset(self):
        profiles = Profile.objects.filter((Q(user__first_name__contains=self.request.GET['text']) | Q(user__last_name__contains=self.request.GET['text']) | Q(user__username__contains=self.request.GET['text'])) & Q(user__is_active=True))
        return profiles
    

class ProfileUpdateView(View):
    """
    Vista externa para actualizar perfil de usuarios.
    """
    template_name = "profile_update.html"
    form_class = ProfileUpdateForm

    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.update(request, pk)
            return redirect('profile', pk)
        else:
            return render(request, self.template_name, {'form':form})


class SingUpView(View):
    """
    Vista para registrar un usuario por la universidad.
    """
    template_name = "signup.html"
    form_class = SignUpForm
    
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            form = self.form_class
            return render(request, self.template_name,{'form':form})
        else:
            return redirect('home')
    
    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.signup(request)
                messages.success(request, f'Usuario añadido correctamente.')
                return redirect('signup')
            else:
                return render(request, self.template_name, {'form':form})
   

def signup_multiple(request):
    """
    Vista para registrar multiples usuarios por parte de la universidad.
    """
    if request.user.is_staff:
        if request.method == 'POST':
            try:
                df = pd.read_excel(request.FILES['file'])
                n = 0
                for i, row in df.iterrows():
                    username = row['EMAIL'].split('@')[0]
                    user, created = User.objects.get_or_create(username=username)
                    if created:
                        n += 1
                        user.first_name = row['NOMBRES'].title()
                        user.last_name = row['APELLIDOS'].title()
                        user.is_active = False
                        user.email = row['EMAIL'].lower()
                        password = secrets.token_urlsafe(8)
                        user.set_password(password)
                        user.save()

                        # Send email
                        current_site = get_current_site(request)
                        email_subject = "Usuario creado."
                        message = f"{current_site.domain}/login, Usuario: {user.username}, Contraseña: {password}"


                        send_mail(
                            email_subject,
                            message,
                            settings.EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=True
                        )
                
                messages.success(request, f'Total de usuarios añadidos: {n}')
            except:
                messages.error(request, "El archivo no coincide con el formato solicitado.")

            return redirect('signup')
        else:
            return redirect('signup')
    else:
        return redirect('home')


def logout_handler(request):
    """
    Manejador de cierre de sesión.
    """
    logout(request)
    return redirect('login')

             


