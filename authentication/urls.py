from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('signup/', views.SingUpView.as_view(), name='signup'),
    path('signup/multiple/', views.signup_multiple, name='signup-multiple'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('activate/', views.ActivateView.as_view(), name='activate'),
    path('profile/list/search/', login_required(views.ProfileSearchListView.as_view()), name='profile-search-list'),
    path('profile/<int:pk>', login_required(views.ProfileDetailView.as_view()), name='profile'),
    path('profile/update/<int:pk>', login_required(views.ProfileUpdateView.as_view()), name='profile-update'),
    path('logout/', views.logout_handler, name='logout'),
]
