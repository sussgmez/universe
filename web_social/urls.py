from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth.views import LoginView
from social_network.views import SingUpView, HomeView, PostCreateView, delete_post, PostListView, ProfileDetailView, SearchView, PostSearchListView, PostProfileListView, PostCommentListView, ProfileSearchListView, ProfileUpdateView, PostDetailView, ChatView, ChatDetailView, MessageCreateView, get_chat, follow, unfollow, activate, logout_handler, like_post


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SingUpView.as_view(), name='signup'),
    path('', login_required(HomeView.as_view()), name='home'),
    path('search/', login_required(SearchView.as_view()), name='search'),
    path('post/create/', login_required(PostCreateView.as_view()), name='post-create'),
    path('post/delete/<int:pk>', delete_post, name='post-delete'),
    path('post/<int:pk>', login_required(PostDetailView.as_view()), name='post'),
    path('post/list/', login_required(PostListView.as_view()), name='post-list'),
    path('post/list/search/', login_required(PostSearchListView.as_view()), name='post-search-list'),
    path('post/list/profile/', login_required(PostProfileListView.as_view()), name='post-profile-list'),
    path('post/list/comment/', login_required(PostCommentListView.as_view()), name='post-comment-list'),
    path('post/like/<int:pk>', like_post, name='like-post'),
    path('profile/list/search/', login_required(ProfileSearchListView.as_view()), name='profile-search-list'),
    path('profile/<int:pk>', login_required(ProfileDetailView.as_view()), name='profile'),
    path('profile/update/<int:pk>', login_required(ProfileUpdateView.as_view()), name='profile-update'),
    path('chat/', login_required(ChatView.as_view()), name='chat'),
    path('chat/<int:pk>', login_required(ChatDetailView.as_view()), name='chat'),
    path('messsage/create/', login_required(MessageCreateView.as_view()), name='message-create'),
    path('chat/get/', get_chat, name='chat-get'),
    path('follow/', follow, name='follow'),
    path('unfollow/', unfollow, name='unfollow'),
    path('activate/', activate, name='activate'),
    path('logout/', logout_handler, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
