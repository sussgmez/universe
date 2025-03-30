from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', views.SingUpView.as_view(), name='signup'),
    path('profile/list/search/', login_required(views.ProfileSearchListView.as_view()), name='profile-search-list'),
    path('profile/<int:pk>', login_required(views.ProfileDetailView.as_view()), name='profile'),
    path('profile/update/<int:pk>', login_required(views.ProfileUpdateView.as_view()), name='profile-update'),
    path('activate/', views.activate, name='activate'),
    path('logout/', views.logout_handler, name='logout'),
]
