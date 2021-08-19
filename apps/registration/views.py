from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('apps.registration:login')
    template_name = 'registration/signup.html'

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/index.html'

