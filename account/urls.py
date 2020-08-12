from django.urls import path
from .views import login_view, profile
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('profile/', profile, name="profile"),
    path("logout/", LogoutView.as_view(), name="logout")
]
