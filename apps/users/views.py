from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from apps.tweet.models import Like, Post

from .forms import SignUpForm
from .models import Connection, User


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('apps.users:login')
    template_name = 'users/registration/signup.html'


class UserProfileView(LoginRequiredMixin, View):
  
    def get(self, request, *args, **kwargs):
      user_data = get_object_or_404(User, username=self.kwargs['username'])
      post_data = Post.objects.filter(user__username=self.kwargs['username'])
      following_data =  Connection.objects.filter(user=user_data).values_list('followee')
      following_count = User.objects.filter(id__in=following_data).count()
      followers_data = user_data.follower.all()
      followers_count = followers_data.count()
      request_user_following_data = Connection.objects.filter(user=self.request.user).values_list('followee')
      request_user_following_list = User.objects.filter(id__in=request_user_following_data) 
      liked_post_pk_list = Like.objects.filter(user=self.request.user).values_list('post', flat=True)
      context = {
        'user_data':user_data, 
        'post_data':post_data, 
        'following_count':following_count, 
        'followers_count':followers_count, 
        'request_user_following_list':request_user_following_list,
        'liked_post_pk_list': liked_post_pk_list,
      }
      return render(request, 'users/profile/profile.html', context)


class FollowBase(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        follower = Connection.objects.get_or_create(user=self.request.user)
        followee = get_object_or_404(User, pk=self.kwargs['pk'])
    
        if follower[0].user.username == followee.username:
            messages.error(request, '自分をフォローすることはできません') 
        elif follower[0].followee.filter(pk=self.kwargs['pk']).exists():
            follower[0].followee.remove(followee)
        else:
            follower[0].followee.add(followee)


class FollowInUserProfile(FollowBase):

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = User.objects.get(pk=self.kwargs['pk'])
        return redirect(reverse('apps.users:profile', kwargs={'username':user.username}))


class FollowingListView(LoginRequiredMixin, ListView):
    model = Connection
    template_name = 'users/profile/following_list.html'

    def get_context_data(self, *args, **kwargs):
      context = super().get_context_data(*args, **kwargs)
      user =  get_object_or_404(User, username=self.kwargs['username'])
      following = Connection.objects.filter(user=user).values_list('followee')
      context['following_list'] = User.objects.filter(id__in=following)
      return context


class FollowersListView(LoginRequiredMixin, ListView):
    model = Connection
    template_name = 'users/profile/followers_list.html'

    def get_context_data(self, *args, **kwargs):
      context = super().get_context_data(*args, **kwargs)
      context['followers_list'] = get_object_or_404(User, username=self.kwargs['username']).follower.all()
      return context
