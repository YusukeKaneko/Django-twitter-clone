from django.urls import include, path

from . import views

app_name = 'apps.registration'


urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('', views.IndexView.as_view(), name="index"),
]
