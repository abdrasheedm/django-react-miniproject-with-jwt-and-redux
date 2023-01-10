from django.urls import path
from .views import LoginView, DeleteView, UserView, UpdateUserView


urlpatterns = [
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('update-user', UpdateUserView.as_view()),
    path('delete', DeleteView.as_view()),
   
]