from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.db.models import Q, Count
from django.urls import reverse
from django.http import HttpResponse
from datetime import date
from datetime import timedelta
from .forms import PublicationForm
from .models import Category, Publication
from authentication.views import Profile


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["publication_form"] = PublicationForm

        min_date = date.today() - timedelta(days= 2)
        context["categories"] = Category.objects.annotate(trend=Count("publication", filter=Q(publication__created__gte=min_date))).order_by('-trend')

        return context
    

class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text"] = self.request.GET['text']
        
        min_date = date.today() - timedelta(days= 2)
        context["categories"] = Category.objects.annotate(trend=Count("publication", filter=Q(publication__created__gte=min_date))).order_by('-trend')
        
        try: context["category_search"] = Category.objects.get(pk=int(self.request.GET['category'])) 
        except: context["category_search"] = 0
        
        return context
    

class PublicationCreateView(CreateView):
    model = Publication
    template_name = "publication_create.html"
    form_class = PublicationForm

    def get(self, request, *args, **kwargs):
        return redirect('home')

    def form_valid(self, form):
        publication = form.save(commit=False)
        publication.author = self.request.user.profile
        publication.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return redirect('home')
    

    def get_success_url(self):
        try:
            return reverse('publication', kwargs={'pk':self.object.commented.pk})
        except: pass
        return reverse('home')


class PublicationDetailView(DetailView):
    model = Publication
    template_name = "publication.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["publication_form"] = PublicationForm
        min_date = date.today() - timedelta(days= 2)
        context["categories"] = Category.objects.annotate(trend=Count("publication", filter=Q(publication__created__gte=min_date))).order_by('-trend')
        return context


class PublicationListView(ListView):
    model = Publication
    template_name = "publication_list.html"
    paginate_by = 10

    def get_queryset(self):
        publications = Publication.objects.filter(author__in=self.request.user.profile.following.all()).filter(commented=None)
        publications = publications.order_by('-created')
        return publications
    

class PublicationSearchListView(ListView):
    model = Publication
    template_name = "publication_list.html"
    paginate_by = 10

    def get_queryset(self):
        category_pk = int(self.request.GET['category'])
        if category_pk != 0:
            publications = Publication.objects.filter(Q(content__contains=self.request.GET['text']) & Q(category=category_pk)).filter(commented=None)
        else:
            publications = Publication.objects.filter(Q(content__contains=self.request.GET['text'])).filter(commented=None)
        publications = publications.order_by('-created')
        return publications
    

class PublicationProfileListView(ListView):
    model = Publication
    template_name = "publication_list.html"
    ordering = ['-created']
    paginate_by = 10

    def get_queryset(self):
        publications = Publication.objects.filter(author=self.kwargs['pk']).filter(commented=None)
        publications = publications.order_by('-created')
        return publications
    

class PublicationCommentListView(ListView):
    model = Publication
    template_name = "publication_list.html"
    ordering = ['-created']
    paginate_by = 10

    def get_queryset(self):
        publications = Publication.objects.filter(commented=self.request.GET['publication'])
        publications = publications.order_by('-created')
        return publications


def like_publication(request, pk):
    if request.method == 'GET':
        publication = Publication.objects.get(pk=pk)
        
        if publication in request.user.profile.liked_publications.all():
            request.user.profile.liked_publications.remove(publication)
            request.user.profile.save()
            lk_publication = len(Profile.objects.filter(liked_publications=publication))
            html = f'<img src="/static/images/hearth_icon.png">{lk_publication}'        
        else:
            request.user.profile.liked_publications.add(publication)
            request.user.profile.save()
            lk_publication = len(Profile.objects.filter(liked_publications=publication))
            html = f'<img src="/static/images/hearth_icon_2.png">{lk_publication}'        


        return HttpResponse(html)


def delete_publication(request, pk):
    if request.method == 'POST':
        Publication.objects.filter(pk=pk).delete()
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

