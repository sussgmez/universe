from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.HomeView.as_view()), name='home'),
    path('search/', login_required(views.SearchView.as_view()), name='search'),
    path('publication/create/', login_required(views.PublicationCreateView.as_view()), name='publication-create'),
    path('publication/delete/<int:pk>', views.delete_publication, name='publication-delete'),
    path('publication/<int:pk>', login_required(views.PublicationDetailView.as_view()), name='publication'),
    path('publication/list/', login_required(views.PublicationListView.as_view()), name='publication-list'),
    path('publication/list/search/', login_required(views.PublicationSearchListView.as_view()), name='publication-search-list'),
    path('publication/list/profile/<int:pk>', login_required(views.PublicationProfileListView.as_view()), name='publication-profile-list'),
    path('publication/list/comment/', login_required(views.PublicationCommentListView.as_view()), name='publication-comment-list'),
    path('publication/like/<int:pk>', views.like_publication, name='like-publication'),
    path('follow/', views.follow, name='follow'),
    path('unfollow/', views.unfollow, name='unfollow'),
]
