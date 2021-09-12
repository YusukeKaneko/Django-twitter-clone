from django.urls import path

from . import views


app_name = 'apps.tweet'


urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('tweet/', views.CreateTweet.as_view(), name='tweet_create'),
    path('detail/<int:pk>', views.DetailTweet.as_view(), name='tweet_detail'),
    path('detail/<int:pk>/delete', views.DeleteTweet.as_view(), name='tweet_delete'),
]
