from django import forms
from .models import Publication


class PublicationForm(forms.ModelForm):
    
    class Meta:
        model = Publication
        fields = ("author", "content", "category", "image", "commented")
        widgets = {
            'content': forms.Textarea(attrs={'rows':'4','placeholder':'Escribe tu publicación acá...'}),
        }
    
