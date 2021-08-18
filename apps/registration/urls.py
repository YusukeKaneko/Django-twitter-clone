from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView

from . import views

app_name = 'apps.registration'

index_view = TemplateView.as_view(template_name="registration/index.html")

urlpatterns = [
    path('', login_required(index_view), name="index"),
    path('', include("django.contrib.auth.urls")),
    path('signup/', views.SignUpView.as_view(), name="signup"),
]
