from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import PostCreateForm
from .models import Post


class HomeView(LoginRequiredMixin, ListView):
   model = Post
   template_name = 'tweet/tweet_list.html'


class CreateTweetView(LoginRequiredMixin, CreateView):
   form_class = PostCreateForm
   template_name = 'tweet/tweet_create.html'

   def get_success_url(self):
        return reverse('apps.users:profile', kwargs={'username': self.request.user.username})
   
   def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)


class DetailTweetView(LoginRequiredMixin, DetailView):
   model = Post
   template_name = 'tweet/tweet_detail.html'


class DeleteTweetView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
   model = Post
   template_name = 'tweet/tweet_delete.html'
   
   def get_success_url(self):
        return reverse('apps.users:profile', kwargs={'username': self.request.user.username})

   def test_func(self, **kwargs):
      pk = self.kwargs["pk"]
      post = get_object_or_404(Post, pk=pk)
      return (post.user == self.request.user) 
