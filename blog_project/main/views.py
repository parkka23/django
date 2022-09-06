from urllib import request, response
from venv import create
from django.contrib.auth.models import User
from . import serializers
from .models import Favourites, Post,Category, Comment, Like
from .permissions import IsAccountOwner, IsAuthor
from rest_framework.status import HTTP_404_NOT_FOUND
# generics based
from rest_framework import generics, permissions
# function based
from rest_framework.decorators import api_view
from rest_framework.response import Response
# class based
from rest_framework.views import APIView
# view set based
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
# for filters
from django_filters.rest_framework import DjangoFilterBackend
# search
from rest_framework.filters import SearchFilter
# pagination
from rest_framework.pagination import PageNumberPagination
# postviewset 
from django.db import connection

# отображение данных пользователю
# generics все api views от у надо наследоваться

class StandartResultPagination(PageNumberPagination):
    page_size=5 # number pf posts
    page_query_param='page' 
    max_page_size=1000

class UserRegistrationView(generics.CreateAPIView):
    queryset=User.objects.all()
    permission_classes=(permissions.AllowAny,)
    serializer_class=serializers.RegisterSerializer

class UserListView(generics.ListAPIView):
    queryset=User.objects.all()
    permission_classes=(permissions.AllowAny,)
    serializer_class=serializers.UserListSerializer

    filter_backends=(SearchFilter,)
    
    search_fields=('username',)

class UserDetailView(generics.RetrieveAPIView):
    queryset=User.objects.all()
    permission_classes=(permissions.IsAuthenticated, IsAccountOwner)
    serializer_class=serializers.UserSerializer

class CategoryListView(generics.ListAPIView):
    queryset=Category.objects.all()
    permission_classes=(permissions.AllowAny,)
    serializer_class=serializers.CategorySerializer


# view set -----------------------------------------------------------------------------------------
# view set регистрировать по роутерам
# http://127.0.0.1:8000/api/v1/posts/posts/
class PostViewSet(ModelViewSet):
    # select_related меньше запросов в бд, меньше времени, меньше нагрузки на бэк
    # макс 2 поля
    queryset=Post.objects.select_related('owner','category',)
    filter_backends=(DjangoFilterBackend,SearchFilter)
    filterset_fields=('category','owner')
    search_fields=('title',)
    pagination_class=StandartResultPagination

    def dispatch(self, request, *args, **kwargs):
        response=super().dispatch(request, *args, **kwargs)
        print('Запросов в бд:', len(connection.queries))
        return response

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return serializers.PostSerializer
        elif self.action in ('create','update','partial_update'):
            return serializers.PostCreateSerializer
        else:
            return serializers.PostListSerializer

    def get_permissions(self):
        # создавать посты может только залогиненный юзер
        # изменять и удалять может только автор поста
        # просматривать могут все
        if self.action in ('create','add_to_liked','remove_from_liked','favourite_action'):
            return [permissions.IsAuthenticated()]
        elif self.action in ('update','partial_update','destroy','get_likes'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        else:
            return [permissions.AllowAny()]

    # comments
    # api/v1/posts/<id>/comments/
    @action(['GET'], detail=True)
    def comments(self, request, pk):
        post=self.get_object()
        comments=post.comments.all()
        serializer=serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    # likes

    # api/v1/posts/<id>/add_to_liked/
    # 1 method like/dislike   one  url
    # @action(['POST'], detail=True)
    # def add_to_liked(self, request, pk):
    #     post=self.get_object()
    #     if request.user.liked.filter(post=post).exists():
    #         # delete like 1 method
    #         request.user.liked.filter(post=post).delete()
    #         return Response('You deleted the like', status=204)
    #     Like.objects.create(post=post, owner=request.user)
    #     return Response('You liked the post', status=201)

    # 2 method  2 diff urls
    @action(['POST'], detail=True)
    def add_to_liked(self, request, pk):
        post=self.get_object()
        if request.user.liked.filter(post=post).exists():
            return Response('You already liked this post', status=400)
        Like.objects.create(post=post, owner=request.user)
        return Response('You liked the post', status=201)

    @action(['POST'], detail=True)
    def remove_from_liked(self, request, pk):
        post=self.get_object()
        if not request.user.liked.filter(post=post).exists():
            return Response('You did not like this post', status=400)
        request.user.liked.filter(post=post).delete()
        return Response('You deleted the like', status=204)

    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        post=self.get_object()
        likes=post.likes.all()
        serializer=serializers.LikeSerializer(likes, many=True)
        return Response(serializer.data, status=200)

    # favourites
    @action(['POST'], detail=True)
    def favourite_action(self, request, pk):
        post=self.get_object()
        if request.user.favourites.filter(post=post).exists():
            request.user.favourites.filter(post=post).delete()
            return Response('This post is deleted from Favourites', status=204)
        Favourites.objects.create(post=post, owner=request.user)
        return Response('This post is added to Favourites', status=201)

    

    
# function based view -----------------------------------------------------------------------------------
# @api_view(['GET'])
# def post_list():
#     posts=Post.objects.all()
#     serializer=serializers.PostSerializer(posts,many=True)
#     return Response(serializer.data)

# class based views(APIView) -------------------------------------------------------------------------------
# class PostView(APIView):
#     # post list
#     def get(self,request):
#         posts=Post.objects.all()
#         serializer=serializers.PostListSerializer(posts, many=True).data
#         return Response(serializer)

#     # create
#     def post(self,request):
#         serializer=serializers.PostCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

# class PostDetailView(APIView):
#     @staticmethod
#     def get_object(pk):
#         try:
#             post=Post.objects.get(pk=pk)
#             return post
#         except Post.DoesNotExist:
#             return False

#     # retrieve
#     def get(self,request,pk):
#         post=self.get_object(pk)
#         if not post:
#             content={
#                 'error':"Invalid id"
#             }
#             return Response(content, status=HTTP_404_NOT_FOUND)
#         serializer=serializers.PostSerializer(post)
#         return Response(serializer.data)

#     # update
#     def put(self,request,pk):
#         post=self.get_object(pk)
#         if not post:
#             content={
#                 'error':"Invalid id"
#             }
#             return Response(content, status=HTTP_404_NOT_FOUND)
#         serializer=serializers.PostCreateSerializer(post,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     # delete
#     def delete(self, request, pk):
#         post=self.get_object(pk)
#         if not post:
#             content={
#                 'error':"Invalid id"
#             }
#             return Response(content, status=HTTP_404_NOT_FOUND)
#         if request.user==post.owner:
#             post.delete()
#             return Response('Deleted',status=204)
#         return Response('Permission denied',status=403)


# CRUD
# generics based views -----------------------------------------------------------------------------

# post listing
# class PostListView(generics.ListAPIView):
#     queryset=Post.objects.all()
#     serializer_class=serializers.PostListSerializer

# create
# class PostCreateView(generics.CreateAPIView):
#     serializer_class=serializers.PostCreateSerializer
#     permission_classes=(permissions.IsAuthenticated,)

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

# # retrieve
# class PostDetailView(generics.RetrieveAPIView):
#     queryset=Post.objects.all()
#     serializer_class=serializers.PostSerializer

# # update
# class PostUpdateView(generics.UpdateAPIView):
#     queryset=Post.objects.all()
#     serializer_class=serializers.PostSerializer
#     permission_classes=(permissions.IsAuthenticated ,IsAuthor)
    
# # delete
# class PostDeleteView(generics.DestroyAPIView):
#     queryset=Post.objects.all()
#     # serializer_class=serializers.PostSerializer
#     permission_classes=(permissions.IsAuthenticated ,IsAuthor)


# integrated generics based comment---------------------------------------------------------------------------------
class CommentListCreateView(generics.ListCreateAPIView):
    queryset=Comment.objects.all()
    serializer_class=serializers.CommentSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=serializers.CommentSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly, IsAuthor)


    
# integrated generics based post---------------------------------------------------------------------------------

# class PostListCreateView(generics.ListCreateAPIView):
#     queryset=Post.objects.all() 

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

#     def get_serializer_class(self):
#         if self.request.method=='GET':
#             return serializers.PostListSerializer
#         else:
#             return serializers.PostCreateSerializer
    
#     def get_permissions(self):
#         if self.request.method=='POST':
#             return (permissions.IsAuthenticated(),)
#         else:
#             return (permissions.AllowAny(),)

# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset=Post.objects.all() 

#     def get_serializer_class(self):
#         if self.request.method in ('PUT', 'PATCH'):
#             return serializers.PostCreateSerializer
#         else:
#             return serializers.PostSerializer
    
#     def get_permissions(self):
#         if self.request.method in ('PUT', 'PATCH','DELETE'):
#             return (permissions.IsAuthenticated(),IsAuthor())
#         else:
#             return (permissions.AllowAny(),)



