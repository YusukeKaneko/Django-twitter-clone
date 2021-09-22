from django.urls import path

from . import views


urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('favorite/', views.LikeTweetView.as_view(), name='favorite'),
    path('tweet/', views.CreateTweetView.as_view(), name='tweet_create'),
    path('detail/<int:pk>/', views.DetailTweetView.as_view(), name='tweet_detail'),
    path('detail/<int:pk>/delete/', views.DeleteTweetView.as_view(), name='tweet_delete'),
    path('like/<int:pk>/', views.LikeTweet.as_view(), name='like'),
    path('unlike/<int:pk>/', views.UnlikeTweet.as_view(), name='unlike'),
]
