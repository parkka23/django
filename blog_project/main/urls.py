from django.urls import path, include
from . import views
# http://localhost:8000 -> views.PostListView

from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('posts', views.PostViewSet, basename='post')

urlpatterns = [
    # path('users/',views.UserListView.as_view()),
    # path('account/register/', views.UserRegistrationView.as_view()),
    path('categories/',views.CategoryListView.as_view()),

    # generics based-----------------------------
    # path('posts/',views.PostListView.as_view()),
    # path('posts/create/',views.PostCreateView.as_view()),
    # path('posts/<int:pk>/',views.PostDetailView.as_view()),
    # path('posts/update/<int:pk>/',views.PostUpdateView.as_view()),
    # path('posts/delete/<int:pk>/',views.PostDeleteView.as_view()),

    # function based-----------------------------
    # path('posts/',views.post_list),  

    # class based--------------------------------
    # path('posts/',views.PostView.as_view()),  
    # path('posts/<int:pk>/',views.PostDetailView.as_view()),

    # view set-----------------------------------
    path('posts/', include(router.urls)), 

    # integrated generics based comment-------------------
    path('comments/', views.CommentListCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()), 

    # integrated generics based-------------------
    # path('posts/', views.PostListCreateView.as_view()), 
    # path('posts/<int:pk>/', views.PostDetailView.as_view()), 

]