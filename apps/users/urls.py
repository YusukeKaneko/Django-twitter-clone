from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views


app_name = 'apps.users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('', include('apps.tweet.urls')),
    path('follow/<int:pk>/', views.FollowInUserProfile.as_view(), name='follow_in_profile'),
    path('<str:username>/', views.UserProfileView.as_view(), name='profile'),
    path('<str:username>/following/', views.FollowingListView.as_view(), name='following_list'),
    path('<str:username>/followers/', views.FollowersListView.as_view(), name='followers_list'),
]
