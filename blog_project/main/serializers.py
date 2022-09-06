from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Category, Favourites, Like, Post, PostImages, Comment

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True, required=True)
    password2 = serializers.CharField(min_length=6, write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs['password'] != password2:
            raise serializers.ValidationError('Passwords did\'t match')
        return attrs

    @staticmethod
    def validate_first_name(value):
        if not value.istitle():
            raise serializers.ValidationError('Name must start with uppercase!')
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data.get('last_name')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Favourites
        fields=('post',)

    def to_representation(self, instance):
        repr= super().to_representation(instance)
        print(instance,'----------------------') # Favourites object (2)
        repr['post']=PostListSerializer(instance.post).data
        print(repr,'--------------------------------') # OrderedDict([('post', {'id': 20, 'title': 'post16', 'preview': '/media/images/cat_eQKFGhF.jpeg'})]) --------------------------------
        return repr
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude=('password',)
    
    def to_representation(self, instance):
        repr=super().to_representation(instance)
        repr['favourites']=FavouriteSerializer(instance.favourites.all(), many=True).data
        return repr

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostImages
        # или fields
        exclude=('id',)

class CommentSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model=Comment
        fields=('id','body','owner','post')

class LikeSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model=Like
        fields=('owner',)


class PostSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField(
        source='owner.username'
    )
    category=serializers.ReadOnlyField(source='category.name')
    images=PostImageSerializer(many=True)
    comments=CommentSerializer(many=True, read_only=True)  # 1 method

    class Meta:
        model=Post
        fields='__all__'
    
    def is_liked(self, post):
        user=self.context.get('request').user
        return user.liked.filter(post=post).exists()

    # 2 method
    def to_representation(self, instance):
        repr=super().to_representation(instance)
        # print(repr,'-----------------------------------------------------------------') # OrderedDict([('id', 20), ('owner', 'admin'), ('category', 'laptop'), ('images', [OrderedDict([('title', ''), ('image', 'http://127.0.0.1:8000/media/images/book.jpeg'), ('post', 20)]), OrderedDict([('title', ''), ('image', 'http://127.0.0.1:8000/media/images/car_ICsOygX.jpg'), ('post', 20)]), OrderedDict([('title', ''), ('image', 'http://127.0.0.1:8000/media/images/cat_A9qsprA.jpeg'), ('post', 20)]), OrderedDict([('title', ''), ('image', 'http://127.0.0.1:8000/media/images/laptop_zRlVySV.png'), ('post', 20)])]), ('title', 'post16'), ('body', 'erferf'), ('preview', 'http://127.0.0.1:8000/media/images/cat_eQKFGhF.jpeg'), ('created_at', '2022-08-11T14:01:24.496655Z'), ('updated_at', '2022-08-11T14:01:24.496680Z')])
        # print(instance) # admin -> post16
        # repr['comments']=CommentSerializer(instance.comments.all(), many=True).data
        user=self.context.get('request').user
        if user.is_authenticated:
            repr['is_liked']=self.is_liked(instance)
        print(instance,'--------------------')
        repr['likes_count']=instance.likes.count()
        return repr

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=('id','title','preview')    

class PostCreateSerializer(serializers.ModelSerializer):
    # owner=serializers.ReadOnlyField(source='owner.username')

    images=PostImageSerializer(many=True, read_only=False, required=False)

    class Meta:
        model=Post
        fields=('title','body','category','preview','images')

    def create(self, validated_data):
        # print('-------------------------------------------')
        # print(validated_data) # {'title': 'post13', 'body': 'erferf', 'category': <Category: laptop>, 'preview': <InMemoryUploadedFile: car.jpg (image/jpeg)>, 'owner': <User: admin>}
        request=self.context.get('request')
        created_post=Post.objects.create(**validated_data)
        images_data=request.FILES
        # print(request.FILES) # <MultiValueDict: {'preview': [<InMemoryUploadedFile: car.jpg (image/jpeg)>], 'images': [<InMemoryUploadedFile: laptop.png (image/png)>]}>
        # print(created_post) # admin - post13
        # print(images_data.getlist('images'))  # [<InMemoryUploadedFile: laptop.png (image/png)>]
        images_object=[PostImages(post=created_post, image=image) for image in images_data.getlist('images')]
        # bulk create - итерируемые объекты tuples, lists
        PostImages.objects.bulk_create(images_object)
        return created_post





