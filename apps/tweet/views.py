from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, View

from .forms import PostCreateForm
from .models import Post, Like


class HomeView(LoginRequiredMixin, View):

   def get (self, request, *args, **kwargs):
      post_list = Post.objects.all()
      liked_list = []
      for post in post_list:
         liked = post.like_set.filter(user=self.request.user)
         if liked.exists():
               liked_list.append(post.pk)
      context = {
         'post_list': post_list,
         'liked_list': liked_list,
      }
      return render(request, 'tweet/tweet_list.html', context)


class LikeTweetView(LoginRequiredMixin, View):

   def get (self, request, *args, **kwargs):
      post_list = Post.objects.all()
      liked_post_list = []
      for post in post_list:
         liked = Like.objects.filter(user=self.request.user, post=post)
         if liked.exists():
               liked_post_list.append(post)
      context = {
         'liked_post_list': liked_post_list,
      }
      return render(request, 'tweet/tweet_like_list.html', context)


class CreateTweetView(LoginRequiredMixin, CreateView):
   form_class = PostCreateForm
   template_name = 'tweet/tweet_create.html'

   def get_success_url(self):
        return reverse('apps.users:profile', kwargs={'username': self.request.user.username})
   
   def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)


class DetailTweetView(LoginRequiredMixin, View):
   
   def get (self, request, *args, **kwargs):
      post = get_object_or_404(Post, pk=self.kwargs["pk"])
      liked_list = request.user.like_set.values_list('post')
      context = {
         'post': post,
         'liked_list': liked_list,
      }
      return render(request, 'tweet/tweet_detail.html', context)


class DeleteTweetView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
   model = Post
   template_name = 'tweet/tweet_delete.html'
   
   def get_success_url(self):
        return reverse('apps.users:profile', kwargs={'username': self.request.user.username})

   def test_func(self, **kwargs):
      pk = self.kwargs['pk']
      post = get_object_or_404(Post, pk=pk)
      return (post.user == self.request.user) 


class LikeTweet(LoginRequiredMixin, View):

   def post(self, request, *args, **kwargs):
      post = get_object_or_404(Post, pk=self.kwargs['pk'])
      like = Like.objects.filter(user=self.request.user, post=post)
      if not like.exists():
         like.create(user=request.user, post=post)
      likes_count = post.like_set.count()
      liked = True
      context = {
         'post_pk': post.pk,
         'likes_count': likes_count,
         'liked': liked,
      }
      return JsonResponse(context)


class UnlikeTweet(LoginRequiredMixin, View):

   def post(self, request, *args, **kwargs):
      post = get_object_or_404(Post, pk=self.kwargs['pk'])
      like = Like.objects.filter(user=self.request.user, post=post)
      if like.exists():
         like.delete()
      likes_count = post.like_set.count()
      liked = False
      context = {
         'post_pk': post.pk,
         'likes_count': likes_count,
         'liked': liked,
      }
      return JsonResponse(context)
