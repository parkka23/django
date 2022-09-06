from django.urls import path
from . import views
from main import views as v

urlpatterns = [
    path('login/', views.CustomLoginView.as_view()),
    path('logout/', views.CustomLogoutView.as_view()),
    path('',v.UserListView.as_view()),
    path('<int:pk>/',v.UserDetailView.as_view()),
    path('register/', v.UserRegistrationView.as_view()),
]