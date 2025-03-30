from django import forms
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

from .tokens import generate_token
from .models import Profile


class SignUpForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'type':'email', 'class':'singup-form__input', 'placeholder':'email@example.com'}), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'singup-form__input', 'placeholder':'usuario1'}), max_length=100, required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'singup-form__input', 'placeholder':'Pepe'}), max_length=100, required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'singup-form__input', 'placeholder':'Pérez'}), max_length=100, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'singup-form__input', 'placeholder':'**********'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'singup-form__input', 'placeholder':'**********'}), required=True)

    class Meta:
        model = User

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(username=username):
            raise forms.ValidationError("Nombre de usuario ya registrado.")
        
        if User.objects.filter(email=email):
            raise forms.ValidationError("Correo electrónico ya registrado.")    

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 != password2:
            raise forms.ValidationError("Contraseñas no coinciden.")
    
    
    def signup(self, request):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password1 = self.cleaned_data.get('password1')
        
        user = User.objects.create(
            username=username, 
            email=email, 
            first_name=first_name, 
            last_name=last_name,
        )

        user.set_password(password1)

        user.is_active = False

        user.save()

        # Send email
        current_site = get_current_site(request)
        email_subject = "Confirmar correo electrónico."
        message = f"{current_site.domain}/activate?uidb64={urlsafe_base64_encode(force_bytes(user.pk))}&token={generate_token.make_token(user)}"

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


    def clean(self):
        pass


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