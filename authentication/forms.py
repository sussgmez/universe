import secrets
import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.mail import send_mail
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'login-form__input', 'placeholder':'Nombre de usuario o Email', 'autofocus':''}), max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'login-form__input', 'placeholder':'Contraseña'}), required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


        if EMAIL_REGEX.match(username):
            user = User.objects.filter(email=username)
            if user:
                username = user[0].username
            else:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")

        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("Usuario o contraseña incorrectos.")
    
    def login(self, request):
        username = self.cleaned_data.get('username')

        if "@" in username:
            username = User.objects.get(email=username).username
        
        user = User.objects.get(username=username)
        login(request, user)


class ActivateForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'type':'email', 'class':'activate-form__input', 'placeholder':'email@example.com', 'autocomplete':'off', 'readonly':'', 'onfocus':"this.removeAttribute('readonly');" }), required=True)
    p_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'activate-form__input', 'placeholder':'••••••••'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'activate-form__input', 'placeholder':'••••••••'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'activate-form__input', 'placeholder':'••••••••'}), required=True)

    class Meta:
        model = User

    def clean(self):
        email = self.cleaned_data.get('email')
        user = User.objects.get(email=email)
        
        if user:
            if not user.is_active:
                password1 = self.cleaned_data.get('password1')
                password2 = self.cleaned_data.get('password2')
                if password1 != password2:
                    raise forms.ValidationError("Contraseñas no coinciden.")
            else:
                raise forms.ValidationError("Usuario se encuentra ya activo.")
        else:
            raise forms.ValidationError("Usuario no registrado en la universidad.")    

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 != password2:
            raise forms.ValidationError("Contraseñas no coinciden.")
    
    
    def activate(self, request):
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        p_password = self.cleaned_data.get('p_password')
        
        user = User.objects.get(email=email)

        if user.check_password(p_password):
        
            user.set_password(password1)

            user.is_active = True

            user.save()

    
class SignUpForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'singup-form__input', 'placeholder':'Alejandro'}), max_length=100, required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'singup-form__input', 'placeholder':'Gómez'}), max_length=100, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'type':'email', 'class':'singup-form__input', 'placeholder':'email@example.com'}), required=True)
    
    class Meta:
        model = User

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError("Usuario ya registrado.")
        
    
    def signup(self, request):
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        
        user = User.objects.create(
            email=email,
            username=email.split("@")[0],
            first_name=first_name,
            last_name=last_name,
        )

        user.is_active = False

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


class ProfileUpdateForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-input', 'placeholder':''}), max_length=100, required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-input', 'placeholder':''}), max_length=100, required=True)
    image = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-input', 'placeholder':''}), max_length=200, required=False)


    def update(self, request, pk):
        profile = Profile.objects.get(pk=pk)
        if request.user == profile.user:    
            profile.user.first_name = request.POST['first_name']
            profile.user.last_name = request.POST['last_name']
            try: profile.image = request.FILES['image']
            except: pass
            profile.description = request.POST['description']

            profile.save()
            profile.user.save()