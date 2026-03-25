from django.urls import path
from .views import SignupView, LoginView, GetUsersView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('users/', GetUsersView.as_view()),
]