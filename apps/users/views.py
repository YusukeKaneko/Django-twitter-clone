from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from apps.tweet.models import Post

from .forms import SignUpForm
from .models import Connection, User


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('apps.users:login')
    template_name = 'registration/signup.html'


class UserProfile(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
      user_data = User.objects.get(username=self.kwargs["username"])
      post_data = Post.objects.filter(user__username=self.kwargs["username"])
      following_data =  Connection.objects.filter(user=user_data).values_list('following')
      following_count = User.objects.filter(id__in=following_data).count()
      followers_data = User.objects.get(username=self.kwargs["username"]).following.all()
      followers_count = followers_data.count()
      request_user_following_data = Connection.objects.filter(user=self.request.user).values_list('following')
      request_user_following_list = User.objects.filter(id__in=request_user_following_data)
      return render(request, 'users/profile.html', {'user_data':user_data, 'post_data':post_data, 'following_count':following_count, 'followers_count':followers_count ,'request_user_following_list':request_user_following_list})


class FollowBase(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        follower = Connection.objects.get_or_create(user=self.request.user)
        following = get_object_or_404(User, pk=self.kwargs["pk"])
    
        if follower[0].user.username == following.username:
            messages.error(request, '自分をフォローすることはできません') 
        elif following in follower[0].following.all():
            follower[0].following.remove(following)
        else:
            follower[0].following.add(following)


class FollowInUserProfile(FollowBase):

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        return redirect(reverse('apps.users:profile', kwargs={'username':user.username}))


class FollowingListView(LoginRequiredMixin, ListView):
    model = Connection
    template_name = 'users/following_list.html'

    def get_context_data(self, *args, **kwargs):
      context = super().get_context_data(*args, **kwargs)
      user =  User.objects.get(username=self.kwargs["username"])
      following = Connection.objects.filter(user=user).values_list('following')
      context['following_list'] = User.objects.filter(id__in=following)
      return context


class FollowersListView(LoginRequiredMixin, ListView):
    model = Connection
    template_name = 'users/followers_list.html'

    def get_context_data(self, *args, **kwargs):
      context = super().get_context_data(*args, **kwargs)
      context['followers_list'] = User.objects.get(username=self.kwargs["username"]).following.all()
      return context