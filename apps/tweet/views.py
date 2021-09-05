from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy

from .models import Post
from .forms import PostCreateForm


class Home(LoginRequiredMixin, ListView):
   model = Post
   template_name = 'tweet/tweet_list.html'
      

class MyTweet(LoginRequiredMixin, ListView):
   model = Post
   template_name = 'tweet/tweet_list.html'

   def get_queryset(self):
       return Post.objects.filter(user=self.request.user)


class CreateTweet(LoginRequiredMixin, CreateView):
   form_class = PostCreateForm
   template_name = 'tweet/tweet_create.html'
   success_url = reverse_lazy('apps.tweet:mytweet')

   def form_valid(self, form):
       form.instance.user = self.request.user
       return super().form_valid(form)


class DetailTweet(LoginRequiredMixin, DetailView):
   model = Post
   template_name = 'tweet/tweet_detail.html'


class DeleteTweet(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
   model = Post
   template_name = 'tweet/tweet_delete.html'
   success_url = reverse_lazy('apps.tweet:mytweet')

   def test_func(self, **kwargs):
       pk = self.kwargs["pk"]
       post = Post.objects.get(pk=pk)
       return (post.user == self.request.user) 
       
